/**
 * OurUI Plasma host escape — minimal WebGL fragment engines.
 * API: Plasma.init(canvasOrId, config) → { destroy() }
 * Modes: gradient | dither | raymarch
 */
(function (global) {
  "use strict";

  const VS = `
    attribute vec2 a_pos;
    void main() { gl_Position = vec4(a_pos, 0.0, 1.0); }
  `;

  const FS_GRADIENT = `
    precision highp float;
    uniform vec2 u_res;
    uniform float u_time;
    uniform float u_pace;
    uniform float u_lens;
    void main() {
      vec2 uv = gl_FragCoord.xy / u_res;
      float t = u_time * (0.15 + u_pace * 0.004);
      vec3 a = vec3(0.42, 0.28, 0.85);
      vec3 b = vec3(0.60, 0.82, 0.08);
      vec3 c = vec3(0.05, 0.05, 0.07);
      float w = sin((uv.x + uv.y) * 3.0 + t) * 0.5 + 0.5;
      float r = length(uv - 0.5) * (1.2 + u_lens * 0.01);
      vec3 col = mix(c, mix(a, b, w), 1.0 - smoothstep(0.2, 1.1, r));
      gl_FragColor = vec4(col, 1.0);
    }
  `;

  const FS_DITHER = `
    precision highp float;
    uniform vec2 u_res;
    uniform float u_time;
    uniform float u_pace;
    uniform float u_texture;
    float hash(vec2 p) {
      return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
    }
    void main() {
      vec2 uv = gl_FragCoord.xy / u_res;
      float t = u_time * (0.2 + u_pace * 0.003);
      float n = hash(floor(uv * (24.0 + u_texture * 0.4)) + t);
      float band = step(0.5, fract(uv.y * 8.0 + t + n * 0.3));
      vec3 dark = vec3(0.04, 0.04, 0.05);
      vec3 mid = vec3(0.42, 0.28, 0.85);
      vec3 lite = vec3(0.60, 0.82, 0.08);
      vec3 col = mix(dark, mix(mid, lite, band), 0.55 + n * 0.45);
      gl_FragColor = vec4(col, 1.0);
    }
  `;

  const FS_RAYMARCH = `
    precision highp float;
    uniform vec2 u_res;
    uniform float u_time;
    uniform float u_pace;
    uniform float u_lens;
    float sdSphere(vec3 p, float r) { return length(p) - r; }
    float map(vec3 p) {
      float t = u_time * (0.3 + u_pace * 0.004);
      p.xz *= mat2(cos(t), -sin(t), sin(t), cos(t));
      return sdSphere(p, 0.55 + u_lens * 0.002);
    }
    void main() {
      vec2 uv = (gl_FragCoord.xy - 0.5 * u_res) / u_res.y;
      vec3 ro = vec3(0.0, 0.0, 2.2);
      vec3 rd = normalize(vec3(uv, -1.4));
      float t = 0.0;
      float hit = 0.0;
      for (int i = 0; i < 48; i++) {
        vec3 p = ro + rd * t;
        float d = map(p);
        if (d < 0.002) { hit = 1.0; break; }
        t += d;
        if (t > 8.0) break;
      }
      vec3 bg = vec3(0.05, 0.05, 0.07);
      vec3 col = mix(bg, vec3(0.42, 0.28, 0.85), hit);
      if (hit > 0.5) {
        vec3 p = ro + rd * t;
        vec3 n = normalize(vec3(
          map(p + vec3(0.01,0,0)) - map(p - vec3(0.01,0,0)),
          map(p + vec3(0,0.01,0)) - map(p - vec3(0,0.01,0)),
          map(p + vec3(0,0,0.01)) - map(p - vec3(0,0,0.01))
        ));
        float light = clamp(dot(n, normalize(vec3(0.4, 0.7, 0.5))), 0.0, 1.0);
        col = mix(vec3(0.20, 0.12, 0.45), vec3(0.60, 0.82, 0.08), light);
      }
      gl_FragColor = vec4(col, 1.0);
    }
  `;

  function compile(gl, type, src) {
    const sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      console.warn("[ourui plasma]", gl.getShaderInfoLog(sh));
      gl.deleteShader(sh);
      return null;
    }
    return sh;
  }

  function makeProgram(gl, fsSrc) {
    const vs = compile(gl, gl.VERTEX_SHADER, VS);
    const fs = compile(gl, gl.FRAGMENT_SHADER, fsSrc);
    if (!vs || !fs) return null;
    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      console.warn("[ourui plasma]", gl.getProgramInfoLog(prog));
      return null;
    }
    return prog;
  }

  function fsFor(mode) {
    if (mode === "dither") return FS_DITHER;
    if (mode === "raymarch") return FS_RAYMARCH;
    return FS_GRADIENT;
  }

  function init(target, config) {
    const cfg = config || {};
    const mode = cfg.mode || "gradient";
    const reduced = cfg.reduced_motion || "static";
    const canvas =
      typeof target === "string" ? document.getElementById(target) || document.querySelector(target) : target;
    if (!canvas || !canvas.getContext) {
      console.warn("[ourui plasma] canvas missing");
      return { destroy: function () {} };
    }

    const prefersReduce =
      typeof matchMedia === "function" && matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReduce && reduced === "static") {
      canvas.classList.add("ourui-canvas-static");
      canvas.dataset.mode = mode;
      return {
        destroy: function () {
          canvas.classList.remove("ourui-canvas-static");
        },
      };
    }

    const gl = canvas.getContext("webgl", { antialias: false, alpha: false });
    if (!gl) {
      canvas.classList.add("ourui-canvas-static");
      return { destroy: function () {} };
    }

    const prog = makeProgram(gl, fsFor(mode));
    if (!prog) {
      return { destroy: function () {} };
    }

    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const aPos = gl.getAttribLocation(prog, "a_pos");
    const uRes = gl.getUniformLocation(prog, "u_res");
    const uTime = gl.getUniformLocation(prog, "u_time");
    const uPace = gl.getUniformLocation(prog, "u_pace");
    const uLens = gl.getUniformLocation(prog, "u_lens");
    const uTexture = gl.getUniformLocation(prog, "u_texture");

    let raf = 0;
    let alive = true;
    const t0 = performance.now();

    function resize() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const w = Math.max(1, Math.floor(canvas.clientWidth * dpr));
      const h = Math.max(1, Math.floor(canvas.clientHeight * dpr));
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
      }
    }

    function frame() {
      if (!alive) return;
      resize();
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.useProgram(prog);
      gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      gl.enableVertexAttribArray(aPos);
      gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);
      gl.uniform2f(uRes, canvas.width, canvas.height);
      gl.uniform1f(uTime, (performance.now() - t0) / 1000);
      gl.uniform1f(uPace, Number(cfg.pace) || 40);
      gl.uniform1f(uLens, Number(cfg.lens) || 30);
      if (uTexture) gl.uniform1f(uTexture, Number(cfg.texture) || 55);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      raf = requestAnimationFrame(frame);
    }

    frame();

    return {
      destroy: function () {
        alive = false;
        if (raf) cancelAnimationFrame(raf);
        try {
          const ext = gl.getExtension("WEBGL_lose_context");
          if (ext) ext.loseContext();
        } catch (_) {}
      },
    };
  }

  global.Plasma = { init: init };
})(typeof window !== "undefined" ? window : globalThis);
