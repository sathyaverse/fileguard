"""
FileGuard – Ultra 3D Cybersecurity Experience (Three.js WebGL Engine)
Renders interactive, cinematic 3D cybersecurity scenes:
- HERO: Massive 3D holographic shield with glowing central lock, dual orbiting energy rings,
        floating 3D file tags (PDF, EXE, IMG, CODE), twinkling particle stars, and mouse-responsive 3D tracking.
- SCANNER: Immersive 3D scanning chamber with rotating rings, animated laser sweep, and floating cyber-file prism.
- RESULT: Dynamic holographic shield in Green (Match), Red (Mismatch alert), or Amber (Unknown) with particle effects.
Includes high-performance Canvas 3D fallback for 100% offline reliability.
"""

import html

def get_threejs_hero_html(mode="HERO", status="SAFE", target_name=None) -> str:
    """
    Generates a self-contained HTML/JS snippet with Three.js WebGL graphics.
    Supports modes: 'HERO', 'SCANNER', 'RESULT'.
    """
    safe_name = html.escape(target_name if target_name else "file_sample.dat")
    mode_upper = mode.upper()
    status_upper = status.upper()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body, html {{
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: transparent;
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }}
    #lab-viewport {{
      width: 100%;
      height: 100%;
      position: relative;
      cursor: grab;
      user-select: none;
    }}
    #lab-viewport:active {{
      cursor: grabbing;
    }}
    canvas {{
      display: block;
      width: 100%;
      height: 100%;
    }}
    /* Cyberpunk HUD Badge Overlay */
    .hud-badge {{
      position: absolute;
      top: 10px;
      right: 12px;
      background: rgba(255, 255, 255, 0.88);
      border: 1px solid rgba(6, 182, 212, 0.45);
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #0284C7;
      backdrop-filter: blur(12px);
      box-shadow: 0 4px 16px rgba(6, 182, 212, 0.2);
      pointer-events: none;
      display: flex;
      align-items: center;
      gap: 6px;
      z-index: 10;
    }}
    .hud-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #06B6D4;
      box-shadow: 0 0 10px #06B6D4;
      animation: hud-pulse 1.4s infinite alternate;
    }}
    @keyframes hud-pulse {{
      0% {{ transform: scale(0.8); opacity: 0.5; }}
      100% {{ transform: scale(1.3); opacity: 1; }}
    }}
    .hud-label-target {{
      position: absolute;
      bottom: 10px;
      left: 12px;
      background: rgba(255, 255, 255, 0.88);
      border: 1px solid rgba(139, 92, 246, 0.35);
      padding: 4px 12px;
      border-radius: 8px;
      font-size: 11px;
      font-family: monospace;
      font-weight: 700;
      color: #4338CA;
      backdrop-filter: blur(10px);
      pointer-events: none;
      z-index: 10;
    }}
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
  <div id="lab-viewport">
    <div class="hud-badge">
      <span class="hud-dot" id="hud-indicator"></span>
      <span id="hud-text">3D LAB READY</span>
    </div>
    <div class="hud-label-target" id="hud-target" style="display: {'block' if mode_upper != 'HERO' else 'none'};">
      TARGET: {safe_name}
    </div>
  </div>

  <script>
  (function() {{
    const mode = "{mode_upper}";
    const status = "{status_upper}";
    const targetFile = "{safe_name}";
    const container = document.getElementById('lab-viewport');
    const hudText = document.getElementById('hud-text');
    const hudDot = document.getElementById('hud-indicator');

    // Update HUD text based on mode and status
    if (mode === "HERO") {{
      hudText.textContent = "3D HOLOGRAM LAB • MOUSE ACTIVE";
    }} else if (mode === "SCANNER") {{
      hudText.textContent = "HOLO-SCANNING CHAMBER ACTIVE";
      hudDot.style.background = "#06B6D4";
      hudDot.style.boxShadow = "0 0 10px #06B6D4";
    }} else if (mode === "RESULT") {{
      if (status === "SAFE") {{
        hudText.textContent = "VERIFIED SAFE SHIELD";
        hudDot.style.background = "#10B981";
        hudDot.style.boxShadow = "0 0 10px #10B981";
      }} else if (status === "SUSPICIOUS") {{
        hudText.textContent = "SECURITY ALERT SHIELD";
        hudDot.style.background = "#EF4444";
        hudDot.style.boxShadow = "0 0 10px #EF4444";
      }} else {{
        hudText.textContent = "UNKNOWN FORMAT SHIELD";
        hudDot.style.background = "#F59E0B";
        hudDot.style.boxShadow = "0 0 10px #F59E0B";
      }}
    }}

    // Check if Three.js is available
    if (typeof THREE === 'undefined') {{
      renderCanvasFallback();
      return;
    }}

    try {{
      initThreeScene();
    }} catch (e) {{
      console.warn("Three.js initialization failed, falling back to Canvas 3D:", e);
      renderCanvasFallback();
    }}

    // =========================================================================
    // PRIMARY THREE.JS WEBGL IMPLEMENTATION
    // =========================================================================
    function initThreeScene() {{
      const width = container.clientWidth || 520;
      const height = container.clientHeight || 340;

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
      camera.position.set(0, 0, mode === "HERO" ? 17 : 14);

      const renderer = new THREE.WebGLRenderer({{ alpha: true, antialias: true, powerPreference: "high-performance" }});
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.2;
      container.appendChild(renderer.domElement);

      // Ambient and Studio Lights
      const ambientLight = new THREE.AmbientLight(0xffffff, 1.1);
      scene.add(ambientLight);

      // Color scheme selector
      let primaryColorHex = 0x3b82f6; // Electric blue
      let emissiveColorHex = 0x06b6d4; // Cyan
      let ringColorHex = 0x06b6d4;
      let secondRingHex = 0x8b5cf6;

      if (mode === "RESULT") {{
        if (status === "SAFE") {{
          primaryColorHex = 0x10b981;
          emissiveColorHex = 0x34d399;
          ringColorHex = 0x10b981;
          secondRingHex = 0x059669;
        }} else if (status === "SUSPICIOUS") {{
          primaryColorHex = 0xef4444;
          emissiveColorHex = 0xf87171;
          ringColorHex = 0xef4444;
          secondRingHex = 0xdc2626;
        }} else {{
          primaryColorHex = 0xf59e0b;
          emissiveColorHex = 0xfbbf24;
          ringColorHex = 0xf59e0b;
          secondRingHex = 0xd97706;
        }}
      }} else if (mode === "SCANNER") {{
        primaryColorHex = 0x06b6d4;
        emissiveColorHex = 0x3b82f6;
        ringColorHex = 0x00f7ff;
        secondRingHex = 0x8b5cf6;
      }}

      const keyLight = new THREE.PointLight(primaryColorHex, 2.8, 50);
      keyLight.position.set(10, 12, 14);
      scene.add(keyLight);

      const fillLight = new THREE.PointLight(emissiveColorHex, 2.2, 50);
      fillLight.position.set(-10, -8, 12);
      scene.add(fillLight);

      const rimLight = new THREE.DirectionalLight(0xffffff, 1.4);
      rimLight.position.set(0, 15, -10);
      scene.add(rimLight);

      // Central Parent Pivot Group for Mouse Parallax
      const mainGroup = new THREE.Group();
      scene.add(mainGroup);

      // -----------------------------------------------------------------------
      // MODE A: HERO SCENE OR RESULT SCENE (3D HOLOGRAPHIC SHIELD & LOCK)
      // -----------------------------------------------------------------------
      let shieldMesh, shieldWireframe, lockGroup, ring1, ring2, scanLaserPlane;
      let fileSprites = [];

      if (mode === "HERO" || mode === "RESULT") {{
        // Build 3D Extruded Shield
        const shieldShape = new THREE.Shape();
        shieldShape.moveTo(0, 3.8);
        shieldShape.quadraticCurveTo(2.8, 3.5, 3.4, 2.6);
        shieldShape.quadraticCurveTo(3.5, 0.2, 3.0, -1.2);
        shieldShape.quadraticCurveTo(1.8, -3.2, 0, -4.2);
        shieldShape.quadraticCurveTo(-1.8, -3.2, -3.0, -1.2);
        shieldShape.quadraticCurveTo(-3.5, 0.2, -3.4, 2.6);
        shieldShape.quadraticCurveTo(-2.8, 3.5, 0, 3.8);

        const extrudeSettings = {{
          depth: 0.6,
          bevelEnabled: true,
          bevelSegments: 4,
          steps: 1,
          bevelSize: 0.25,
          bevelThickness: 0.25
        }};

        const shieldGeom = new THREE.ExtrudeGeometry(shieldShape, extrudeSettings);
        shieldGeom.center();

        const shieldMat = new THREE.MeshPhysicalMaterial({{
          color: primaryColorHex,
          emissive: emissiveColorHex,
          emissiveIntensity: mode === "RESULT" && status === "SUSPICIOUS" ? 0.6 : 0.35,
          roughness: 0.15,
          metalness: 0.15,
          transmission: 0.65,
          transparent: true,
          opacity: 0.9,
          clearcoat: 1.0,
          clearcoatRoughness: 0.1
        }});

        shieldMesh = new THREE.Mesh(shieldGeom, shieldMat);
        mainGroup.add(shieldMesh);

        // Holographic Wireframe Cage
        const wireframeGeom = new THREE.WireframeGeometry(shieldGeom);
        const wireframeMat = new THREE.LineBasicMaterial({{
          color: mode === "RESULT" && status === "SUSPICIOUS" ? 0xff4d4d : 0xa5f3fc,
          transparent: true,
          opacity: 0.55
        }});
        shieldWireframe = new THREE.LineSegments(wireframeGeom, wireframeMat);
        mainGroup.add(shieldWireframe);

        // Central Padlock (or Symbol)
        lockGroup = new THREE.Group();

        // Shackle Arc
        const shackleGeom = new THREE.TorusGeometry(0.72, 0.18, 16, 32, Math.PI);
        const shackleMat = new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.2, metalness: 0.85 }});
        const shackleMesh = new THREE.Mesh(shackleGeom, shackleMat);
        shackleMesh.position.set(0, 0.62, 0.42);
        lockGroup.add(shackleMesh);

        // Body
        const lockBodyGeom = new THREE.BoxGeometry(1.65, 1.35, 0.48);
        const lockBodyMat = new THREE.MeshStandardMaterial({{
          color: mode === "RESULT" && status === "SUSPICIOUS" ? 0x991b1b : 0x4f46e5,
          emissive: emissiveColorHex,
          emissiveIntensity: 0.4,
          metalness: 0.6,
          roughness: 0.25
        }});
        const lockBodyMesh = new THREE.Mesh(lockBodyGeom, lockBodyMat);
        lockBodyMesh.position.set(0, -0.15, 0.42);
        lockGroup.add(lockBodyMesh);

        // Glowing Core Symbol
        const coreGeom = new THREE.SphereGeometry(0.2, 16, 16);
        const coreMat = new THREE.MeshBasicMaterial({{
          color: mode === "RESULT" && status === "SUSPICIOUS" ? 0xffffff : 0x00f7ff
        }});
        const coreMesh = new THREE.Mesh(coreGeom, coreMat);
        coreMesh.position.set(0, -0.1, 0.68);
        lockGroup.add(coreMesh);

        mainGroup.add(lockGroup);

        // Orbiting Energy Ring 1
        const ring1Geom = new THREE.TorusGeometry(5.2, 0.08, 16, 100);
        const ring1Mat = new THREE.MeshBasicMaterial({{ color: ringColorHex }});
        ring1 = new THREE.Mesh(ring1Geom, ring1Mat);
        ring1.rotation.x = Math.PI / 2.7;
        ring1.rotation.y = Math.PI / 12;
        mainGroup.add(ring1);

        // Orbiting Energy Ring 2
        const ring2Geom = new THREE.TorusGeometry(4.3, 0.07, 16, 100);
        const ring2Mat = new THREE.MeshBasicMaterial({{ color: secondRingHex }});
        ring2 = new THREE.Mesh(ring2Geom, ring2Mat);
        ring2.rotation.x = Math.PI / 2.3;
        ring2.rotation.y = -Math.PI / 7;
        mainGroup.add(ring2);

        // Holographic Platform Disc at Base
        const platformDisc = new THREE.Mesh(
          new THREE.CylinderGeometry(4.2, 4.4, 0.25, 32),
          new THREE.MeshStandardMaterial({{ color: 0xe0e7ff, transparent: true, opacity: 0.75 }})
        );
        platformDisc.position.y = -4.5;
        mainGroup.add(platformDisc);

        const platformGlow = new THREE.Mesh(
          new THREE.RingGeometry(2.2, 4.2, 32),
          new THREE.MeshBasicMaterial({{ color: ringColorHex, side: THREE.DoubleSide, transparent: true, opacity: 0.6 }})
        );
        platformGlow.rotation.x = -Math.PI / 2;
        platformGlow.position.y = -4.35;
        mainGroup.add(platformGlow);

        // Floating 3D File Format Tiles (HERO MODE ONLY)
        if (mode === "HERO") {{
          function makeTile(label, bg, fg, r, offset) {{
            const c = document.createElement('canvas');
            c.width = 128;
            c.height = 64;
            const ctx = c.getContext('2d');
            ctx.fillStyle = bg;
            ctx.beginPath();
            ctx.roundRect(4, 4, 120, 56, 14);
            ctx.fill();
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 4;
            ctx.stroke();

            ctx.font = 'bold 26px sans-serif';
            ctx.fillStyle = fg;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(label, 64, 34);

            const tex = new THREE.CanvasTexture(c);
            const sprMat = new THREE.SpriteMaterial({{ map: tex, transparent: true }});
            const spr = new THREE.Sprite(sprMat);
            spr.scale.set(1.9, 0.95, 1);
            return {{ spr, r, offset }};
          }}

          const tiles = [
            makeTile('📄 PDF', 'rgba(239, 68, 68, 0.92)', '#ffffff', 5.8, 0),
            makeTile('⚙️ EXE', 'rgba(124, 58, 237, 0.92)', '#ffffff', 6.2, Math.PI / 2),
            makeTile('🖼️ IMG', 'rgba(6, 182, 212, 0.92)', '#ffffff', 5.6, Math.PI),
            makeTile('</> CODE', 'rgba(37, 99, 235, 0.92)', '#ffffff', 6.0, (Math.PI * 3) / 2)
          ];
          tiles.forEach(t => {{
            mainGroup.add(t.spr);
            fileSprites.push(t);
          }});
        }}

      // -----------------------------------------------------------------------
      // MODE B: SCANNER SCENE (CYBER SCANNING CHAMBER + LASER)
      // -----------------------------------------------------------------------
      }} else if (mode === "SCANNER") {{
        // Holographic Cyber File Prism (floating object inside chamber)
        const docGeom = new THREE.BoxGeometry(2.8, 3.8, 0.35);
        const docMat = new THREE.MeshPhysicalMaterial({{
          color: 0x38bdf8,
          emissive: 0x06b6d4,
          emissiveIntensity: 0.45,
          roughness: 0.1,
          metalness: 0.2,
          transmission: 0.7,
          transparent: true,
          opacity: 0.85
        }});
        shieldMesh = new THREE.Mesh(docGeom, docMat);
        mainGroup.add(shieldMesh);

        // Document wireframe outline
        const docWireGeom = new THREE.WireframeGeometry(docGeom);
        const docWireMat = new THREE.LineBasicMaterial({{ color: 0x00f7ff, transparent: true, opacity: 0.75 }});
        shieldWireframe = new THREE.LineSegments(docWireGeom, docWireMat);
        mainGroup.add(shieldWireframe);

        // Concentric Holographic Scanner Rings
        const scanRing1 = new THREE.Mesh(
          new THREE.TorusGeometry(3.6, 0.08, 16, 80),
          new THREE.MeshBasicMaterial({{ color: 0x06b6d4 }})
        );
        scanRing1.rotation.x = Math.PI / 2;
        mainGroup.add(scanRing1);
        ring1 = scanRing1;

        const scanRing2 = new THREE.Mesh(
          new THREE.TorusGeometry(4.2, 0.06, 16, 80),
          new THREE.MeshBasicMaterial({{ color: 0x8b5cf6 }})
        );
        scanRing2.rotation.x = Math.PI / 2;
        mainGroup.add(scanRing2);
        ring2 = scanRing2;

        // Oscillating Glowing Laser Scanning Sheet
        const laserGeom = new THREE.PlaneGeometry(4.4, 0.2);
        const laserMat = new THREE.MeshBasicMaterial({{
          color: 0x00f7ff,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0.95
        }});
        scanLaserPlane = new THREE.Mesh(laserGeom, laserMat);
        mainGroup.add(scanLaserPlane);
      }}

      // -----------------------------------------------------------------------
      // PARTICLE FIELD (1,000 SPARKLE STARS & CYBER ENERGY DUST)
      // -----------------------------------------------------------------------
      const count = mode === "HERO" ? 1100 : 700;
      const pGeom = new THREE.BufferGeometry();
      const pPos = new Float32Array(count * 3);
      const pCol = new Float32Array(count * 3);

      const colorList = [
        new THREE.Color(ringColorHex),
        new THREE.Color(secondRingHex),
        new THREE.Color(0xffffff),
        new THREE.Color(0x38bdf8)
      ];

      for (let i = 0; i < count; i++) {{
        pPos[i * 3] = (Math.random() - 0.5) * 32;
        pPos[i * 3 + 1] = (Math.random() - 0.5) * 22;
        pPos[i * 3 + 2] = (Math.random() - 0.5) * 22;

        const c = colorList[Math.floor(Math.random() * colorList.length)];
        pCol[i * 3] = c.r;
        pCol[i * 3 + 1] = c.g;
        pCol[i * 3 + 2] = c.b;
      }}

      pGeom.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
      pGeom.setAttribute('color', new THREE.BufferAttribute(pCol, 3));

      // Create radiant diamond star glitter sprite texture
      function createGlitterSprite() {{
        const c = document.createElement('canvas');
        c.width = 64;
        c.height = 64;
        const gctx = c.getContext('2d');
        const radial = gctx.createRadialGradient(32, 32, 0, 32, 32, 30);
        radial.addColorStop(0, 'rgba(255, 255, 255, 1)');
        radial.addColorStop(0.3, 'rgba(6, 182, 212, 0.85)');
        radial.addColorStop(0.65, 'rgba(139, 92, 246, 0.45)');
        radial.addColorStop(1, 'rgba(0, 0, 0, 0)');
        gctx.fillStyle = radial;
        gctx.beginPath();
        gctx.arc(32, 32, 30, 0, Math.PI * 2);
        gctx.fill();

        // 4-point star spike flare
        gctx.strokeStyle = '#FFFFFF';
        gctx.lineWidth = 3;
        gctx.beginPath();
        gctx.moveTo(32, 4); gctx.lineTo(32, 60);
        gctx.moveTo(4, 32); gctx.lineTo(60, 32);
        gctx.stroke();

        return new THREE.CanvasTexture(c);
      }}

      const pMat = new THREE.PointsMaterial({{
        size: 0.65,
        map: createGlitterSprite(),
        vertexColors: true,
        transparent: true,
        opacity: 0.95,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      }});
      const starParticles = new THREE.Points(pGeom, pMat);
      scene.add(starParticles);

      // -----------------------------------------------------------------------
      // INTERACTIVE MOUSE TRACKING & PARALLAX
      // -----------------------------------------------------------------------
      let mouseX = 0;
      let mouseY = 0;
      let targetRotY = 0;
      let targetRotX = 0;

      window.addEventListener('mousemove', (e) => {{
        const rect = container.getBoundingClientRect();
        const normX = ((e.clientX - rect.left) / width) * 2 - 1;
        const normY = -(((e.clientY - rect.top) / height) * 2 - 1);
        mouseX = normX * 0.55;
        mouseY = normY * 0.35;
      }});

      window.addEventListener('resize', () => {{
        const w = container.clientWidth;
        const h = container.clientHeight;
        if (w && h) {{
          camera.aspect = w / h;
          camera.updateProjectionMatrix();
          renderer.setSize(w, h);
        }}
      }});

      // -----------------------------------------------------------------------
      // 60 FPS ANIMATION LOOP
      // -----------------------------------------------------------------------
      const clock = new THREE.Clock();

      function animate() {{
        requestAnimationFrame(animate);
        const t = clock.getElapsedTime();

        // Smooth mouse damping
        targetRotY += (mouseX - targetRotY) * 0.05;
        targetRotX += (mouseY - targetRotX) * 0.05;

        mainGroup.rotation.y = targetRotY + Math.sin(t * 0.6) * 0.15;
        mainGroup.rotation.x = -targetRotX + Math.cos(t * 0.8) * 0.08;

        if (shieldMesh) {{
          shieldMesh.position.y = Math.sin(t * 1.6) * 0.22;
          if (shieldWireframe) shieldWireframe.position.y = shieldMesh.position.y;
          if (lockGroup) lockGroup.position.y = shieldMesh.position.y;
        }}

        // Ring animations
        if (ring1) ring1.rotation.z = t * (mode === "SCANNER" ? 1.5 : 0.8);
        if (ring2) ring2.rotation.z = -t * (mode === "SCANNER" ? 1.8 : 0.6);

        // Laser scan sweep in chamber mode
        if (scanLaserPlane) {{
          scanLaserPlane.position.y = Math.sin(t * 3.2) * 2.1;
          scanLaserPlane.material.opacity = 0.7 + Math.sin(t * 6.0) * 0.3;
        }}

        // Orbiting file sprites in Hero mode
        fileSprites.forEach((tile, idx) => {{
          const angle = t * 0.45 + tile.offset;
          tile.spr.position.x = Math.cos(angle) * tile.r;
          tile.spr.position.z = Math.sin(angle) * 3.4;
          tile.spr.position.y = Math.sin(t * 1.8 + idx) * 0.45 + (idx % 2 === 0 ? 1.2 : -1.0);
        }});

        // Ambient particles slow orbit
        starParticles.rotation.y = t * 0.03;
        starParticles.rotation.x = Math.sin(t * 0.02) * 0.04;

        renderer.render(scene, camera);
      }}

      animate();
    }}

    // =========================================================================
    // GRACEFUL 3D CANVAS FALLBACK (GUARANTEES 100% OFFLINE RENDERING)
    // =========================================================================
    function renderCanvasFallback() {{
      const cvs = document.createElement('canvas');
      cvs.width = container.clientWidth || 520;
      cvs.height = container.clientHeight || 340;
      container.appendChild(cvs);
      const ctx = cvs.getContext('2d');

      let mouseX = 0;
      let mouseY = 0;
      window.addEventListener('mousemove', (e) => {{
        const rect = container.getBoundingClientRect();
        mouseX = ((e.clientX - rect.left) / cvs.width) * 2 - 1;
        mouseY = ((e.clientY - rect.top) / cvs.height) * 2 - 1;
      }});

      let start = performance.now();
      function draw() {{
        requestAnimationFrame(draw);
        const t = (performance.now() - start) * 0.001;
        ctx.clearRect(0, 0, cvs.width, cvs.height);

        const cx = cvs.width / 2 + mouseX * 24;
        const cy = cvs.height / 2 + mouseY * 16;

        // Base Pedestal Glow
        ctx.save();
        ctx.translate(cx, cy + 95);
        ctx.scale(1, 0.3);
        const grad = ctx.createRadialGradient(0, 0, 10, 0, 0, 130);
        grad.addColorStop(0, 'rgba(6, 182, 212, 0.6)');
        grad.addColorStop(0.6, 'rgba(59, 130, 246, 0.25)');
        grad.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(0, 0, 130, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // Orbiting Rings
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(Math.sin(t * 0.5) * 0.2 + mouseX * 0.3);

        ctx.strokeStyle = '#06B6D4';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.ellipse(0, 0, 140, 50, t * 0.8, 0, Math.PI * 2);
        ctx.stroke();

        ctx.strokeStyle = '#8B5CF6';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.ellipse(0, 0, 125, 42, -t * 0.6, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();

        // 3D Floating Shield
        ctx.save();
        const shieldY = cy + Math.sin(t * 1.8) * 8 - 10;
        ctx.translate(cx, shieldY);
        ctx.scale(1.15, 1.15);

        // Shield gradient fill
        const sGrad = ctx.createLinearGradient(-45, -55, 45, 60);
        if (mode === "RESULT" && status === "SUSPICIOUS") {{
          sGrad.addColorStop(0, '#EF4444');
          sGrad.addColorStop(1, '#991B1B');
        }} else if (mode === "RESULT" && status === "SAFE") {{
          sGrad.addColorStop(0, '#10B981');
          sGrad.addColorStop(1, '#047857');
        }} else {{
          sGrad.addColorStop(0, '#38BDF8');
          sGrad.addColorStop(0.5, '#3B82F6');
          sGrad.addColorStop(1, '#7C3AED');
        }}

        ctx.fillStyle = sGrad;
        ctx.beginPath();
        ctx.moveTo(0, -60);
        ctx.quadraticCurveTo(45, -52, 50, -25);
        ctx.quadraticCurveTo(52, 20, 0, 65);
        ctx.quadraticCurveTo(-52, 20, -50, -25);
        ctx.quadraticCurveTo(-45, -52, 0, -60);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 3;
        ctx.stroke();

        // Inner Padlock
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(0, -14, 13, Math.PI, 0);
        ctx.stroke();

        ctx.fillStyle = '#FFFFFF';
        ctx.beginPath();
        ctx.roundRect(-16, -12, 32, 26, 6);
        ctx.fill();

        ctx.fillStyle = '#1E293B';
        ctx.beginPath();
        ctx.arc(0, -1, 3.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // Floating file badges
        if (mode === "HERO") {{
          const badges = [
            {{ name: '📄 PDF', color: '#EF4444', angle: t * 0.45 }},
            {{ name: '⚙️ EXE', color: '#8B5CF6', angle: t * 0.45 + Math.PI / 2 }},
            {{ name: '🖼️ IMG', color: '#06B6D4', angle: t * 0.45 + Math.PI }},
            {{ name: '</> CODE', color: '#2563EB', angle: t * 0.45 + 3 * Math.PI / 2 }}
          ];
          badges.forEach(b => {{
            const bx = cx + Math.cos(b.angle) * 120;
            const by = cy + Math.sin(b.angle) * 45 + Math.sin(t * 2 + b.angle) * 8;
            ctx.fillStyle = b.color;
            ctx.beginPath();
            ctx.roundRect(bx - 32, by - 14, 64, 28, 8);
            ctx.fill();
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 12px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(b.name, bx, by + 4);
          }});
        }}
      }}
      draw();
    }}

  }})();
  </script>
</body>
</html>"""
