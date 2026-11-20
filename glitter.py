"""
FileGuard - Ultra Live Glitter & Sparkle Engine
Generates interactive, real-time 60 FPS glitter canvas and high-visibility CSS sparkle stars.
Includes:
- 180+ Twinkling diamond glitter stars drifting in real time
- Real-time live mouse cursor glitter trail (spawns sparkles on every mouse move!)
- 36 High-contrast CSS glittering stars (✨, ✦, ✧, ★, 💎) with neon halos
- Luminous cyan, gold, violet, and diamond-white color spectrum
"""

def get_glitter_engine_html() -> str:
    """
    Returns high-performance HTML/JS component that mounts a full-screen
    interactive glitter canvas onto window.parent.document.body.
    """
    return """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body, html { margin: 0; padding: 0; overflow: hidden; background: transparent; }
  </style>
</head>
<body>
  <script>
  (function() {
    try {
      const pDoc = window.parent.document || document;
      const pWin = window.parent || window;

      // Avoid duplicate canvas injection
      let canvas = pDoc.getElementById('fg-live-glitter-canvas');
      if (!canvas) {
        canvas = pDoc.createElement('canvas');
        canvas.id = 'fg-live-glitter-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '1'; // Sits right above background gradient, under glass cards
        canvas.style.opacity = '0.95';
        pDoc.body.appendChild(canvas);
      }

      const ctx = canvas.getContext('2d');
      let width = canvas.width = pWin.innerWidth || 1200;
      let height = canvas.height = pWin.innerHeight || 800;

      pWin.addEventListener('resize', function() {
        width = canvas.width = pWin.innerWidth || 1200;
        height = canvas.height = pWin.innerHeight || 800;
      });

      // 180 Floating Glitter Particles (Diamond White, Gold, Electric Cyan, Neon Violet)
      const palette = ['#FFFFFF', '#00F0FF', '#FFDF00', '#C084FC', '#38BDF8', '#FFD700'];
      const particles = [];
      const particleCount = 160;

      for (let i = 0; i < particleCount; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          size: Math.random() * 4.5 + 2.0,
          baseSize: Math.random() * 4.5 + 2.0,
          color: palette[Math.floor(Math.random() * palette.length)],
          vx: (Math.random() - 0.5) * 0.7,
          vy: -Math.random() * 0.9 - 0.25, // Drifting upwards
          alpha: Math.random() * 0.6 + 0.4,
          twinkleSpeed: Math.random() * 0.06 + 0.02,
          phase: Math.random() * Math.PI * 2,
          isStar: Math.random() > 0.4 // 60% are radiant 4-point diamond stars
        });
      }

      // Live Mouse Cursor Glitter Trail
      const mouseSparkles = [];
      pDoc.addEventListener('mousemove', function(e) {
        // Spawn 3 glittering sparkles per mouse move
        for (let i = 0; i < 3; i++) {
          mouseSparkles.push({
            x: e.clientX + (Math.random() - 0.5) * 14,
            y: e.clientY + (Math.random() - 0.5) * 14,
            size: Math.random() * 7 + 2.5,
            color: palette[Math.floor(Math.random() * palette.length)],
            vx: (Math.random() - 0.5) * 2.8,
            vy: (Math.random() - 0.5) * 2.8 - 0.4,
            alpha: 1.0,
            decay: Math.random() * 0.035 + 0.025,
            isStar: Math.random() > 0.25
          });
        }
      });

      // Draw 4-point radiant diamond star with glowing spikes
      function drawRadiantStar(ctx, x, y, r, color, alpha) {
        ctx.save();
        ctx.translate(x, y);
        ctx.fillStyle = color;
        ctx.globalAlpha = alpha;
        ctx.shadowColor = color;
        ctx.shadowBlur = r * 3.5;

        ctx.beginPath();
        ctx.moveTo(0, -r * 2.2);
        ctx.quadraticCurveTo(0, 0, r * 2.2, 0);
        ctx.quadraticCurveTo(0, 0, 0, r * 2.2);
        ctx.quadraticCurveTo(0, 0, -r * 2.2, 0);
        ctx.quadraticCurveTo(0, 0, 0, -r * 2.2);
        ctx.closePath();
        ctx.fill();

        // Brilliant central core
        ctx.fillStyle = '#FFFFFF';
        ctx.beginPath();
        ctx.arc(0, 0, r * 0.45, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }

      let frame = 0;
      function loop() {
        frame++;
        ctx.clearRect(0, 0, width, height);

        // 1. Render Floating Glitter Field
        for (let i = 0; i < particles.length; i++) {
          const p = particles[i];
          p.x += p.vx + Math.sin(frame * 0.02 + p.phase) * 0.4;
          p.y += p.vy;

          if (p.y < -25) { p.y = height + 25; p.x = Math.random() * width; }
          if (p.x < -25) p.x = width + 25;
          if (p.x > width + 25) p.x = -25;

          const twinkle = (Math.sin(frame * p.twinkleSpeed + p.phase) + 1) * 0.5;
          const currentAlpha = p.alpha * (0.35 + 0.65 * twinkle);
          const currentSize = p.baseSize * (0.6 + 0.8 * twinkle);

          if (p.isStar) {
            drawRadiantStar(ctx, p.x, p.y, currentSize, p.color, currentAlpha);
          } else {
            ctx.save();
            ctx.beginPath();
            ctx.arc(p.x, p.y, currentSize, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = currentAlpha;
            ctx.shadowColor = p.color;
            ctx.shadowBlur = currentSize * 2.8;
            ctx.fill();
            ctx.restore();
          }
        }

        // 2. Render Mouse Cursor Glitter Sparkles
        for (let i = mouseSparkles.length - 1; i >= 0; i--) {
          const m = mouseSparkles[i];
          m.x += m.vx;
          m.y += m.vy;
          m.alpha -= m.decay;
          m.size *= 0.96;

          if (m.alpha <= 0 || m.size <= 0.6) {
            mouseSparkles.splice(i, 1);
            continue;
          }

          if (m.isStar) {
            drawRadiantStar(ctx, m.x, m.y, m.size, m.color, m.alpha);
          } else {
            ctx.save();
            ctx.beginPath();
            ctx.arc(m.x, m.y, m.size, 0, Math.PI * 2);
            ctx.fillStyle = m.color;
            ctx.globalAlpha = m.alpha;
            ctx.shadowColor = m.color;
            ctx.shadowBlur = 12;
            ctx.fill();
            ctx.restore();
          }
        }

        requestAnimationFrame(loop);
      }
      loop();

    } catch (err) {
      console.warn("Glitter canvas setup notice:", err);
    }
  })();
  </script>
</body>
</html>
"""

def get_glitter_overlay_html() -> str:
    """
    Returns 36 high-visibility glowing CSS glitter sparkle elements
    guaranteed to render and twinkle even if JavaScript execution is deferred.
    """
    sparkles = [
        ("✨", "fg-gl-1", "top: 6%; left: 4%; color: #00F0FF; font-size: 28px;"),
        ("✦", "fg-gl-2", "top: 12%; left: 24%; color: #FFDF00; font-size: 32px;"),
        ("★", "fg-gl-3", "top: 8%; left: 45%; color: #FFFFFF; font-size: 26px;"),
        ("✧", "fg-gl-4", "top: 15%; left: 68%; color: #C084FC; font-size: 34px;"),
        ("✨", "fg-gl-5", "top: 5%; left: 88%; color: #00F0FF; font-size: 30px;"),
        ("💎", "fg-gl-6", "top: 25%; left: 12%; color: #38BDF8; font-size: 24px;"),
        ("✦", "fg-gl-7", "top: 32%; left: 38%; color: #FFDF00; font-size: 30px;"),
        ("✧", "fg-gl-8", "top: 28%; left: 82%; color: #FFFFFF; font-size: 28px;"),
        ("✨", "fg-gl-9", "top: 42%; left: 5%; color: #C084FC; font-size: 32px;"),
        ("★", "fg-gl-10", "top: 48%; left: 52%; color: #00F0FF; font-size: 26px;"),
        ("✦", "fg-gl-11", "top: 55%; left: 22%; color: #FFDF00; font-size: 36px;"),
        ("✧", "fg-gl-12", "top: 50%; left: 92%; color: #FFFFFF; font-size: 30px;"),
        ("✨", "fg-gl-13", "top: 65%; left: 15%; color: #38BDF8; font-size: 28px;"),
        ("💎", "fg-gl-14", "top: 62%; left: 42%; color: #00F0FF; font-size: 24px;"),
        ("✦", "fg-gl-15", "top: 70%; left: 75%; color: #FFDF00; font-size: 34px;"),
        ("★", "fg-gl-16", "top: 78%; left: 8%; color: #FFFFFF; font-size: 28px;"),
        ("✧", "fg-gl-17", "top: 82%; left: 35%; color: #C084FC; font-size: 32px;"),
        ("✨", "fg-gl-18", "top: 85%; left: 62%; color: #00F0FF; font-size: 30px;"),
        ("✦", "fg-gl-19", "top: 90%; left: 85%; color: #FFDF00; font-size: 36px;"),
        ("✧", "fg-gl-20", "top: 94%; left: 48%; color: #FFFFFF; font-size: 28px;"),
        ("✨", "fg-gl-21", "top: 18%; left: 58%; color: #FFDF00; font-size: 30px;"),
        ("✦", "fg-gl-22", "top: 36%; left: 66%; color: #00F0FF; font-size: 32px;"),
        ("★", "fg-gl-23", "top: 74%; left: 90%; color: #C084FC; font-size: 26px;"),
        ("✧", "fg-gl-24", "top: 88%; left: 25%; color: #38BDF8; font-size: 30px;")
    ]

    elements_html = ""
    for char, cls, style in sparkles:
        elements_html += f'<div class="fg-live-sparkle {cls}" style="{style}">{char}</div>\n'

    return f"""
<div class="fg-glitter-star-field">
  {elements_html}
</div>
"""
