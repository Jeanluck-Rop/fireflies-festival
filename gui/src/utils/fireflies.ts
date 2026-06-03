export interface Firefly {
  x: number
  y: number
  r: number
  vx: number
  vy: number
  a: number
  s: number
  o: number
}

export interface FirefliesOptions {
  count?: number
  color?: string
}

export function startFireflies(
  canvas: HTMLCanvasElement,
  options: FirefliesOptions = {}
) {
  const ctx = canvas.getContext('2d')
  if (!ctx) return () => {}

  const count = options.count ?? 60
  const color = options.color ?? '245,213,122'

  let w = 0
  let h = 0
  let dpr = 1

  let animationFrameId = 0
  let flies: Firefly[] = []

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2)

    w = canvas.clientWidth
    h = canvas.clientHeight

    canvas.width = w * dpr
    canvas.height = h * dpr

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  }

  function spawn() {
    flies = Array.from({ length: count }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: 0.8 + Math.random() * 2,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      a: Math.random() * Math.PI * 2,
      s: 0.005 + Math.random() * 0.02,
      o: 0.3 + Math.random() * 0.5,
    }))
  }

  function draw(t: number) {
    ctx.clearRect(0, 0, w, h)

    for (const f of flies) {
      f.a += f.s

      f.x += Math.cos(f.a) * f.vx
      f.y += Math.sin(f.a) * f.vy - 0.15

      // Wrap screen
      if (f.x < -20) f.x = w + 20
      if (f.x > w + 20) f.x = -20
      if (f.y < -20) f.y = h + 20
      if (f.y > h + 20) f.y = -20

      // Pulse animation
      const pulse = 0.5 + 0.5 * Math.sin(t * 0.002 + f.a)
      const opacity = f.o * pulse

      // Glow
      const gradient = ctx.createRadialGradient(
        f.x,
        f.y,
        0,
        f.x,
        f.y,
        f.r * 10
      )

      gradient.addColorStop(0, `rgba(${color},${opacity})`)
      gradient.addColorStop(0.4, `rgba(${color},${opacity * 0.4})`)
      gradient.addColorStop(1, `rgba(${color},0)`)

      ctx.fillStyle = gradient

      ctx.beginPath()
      ctx.arc(f.x, f.y, f.r * 10, 0, Math.PI * 2)
      ctx.fill()

      // Core
      ctx.beginPath()
      ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(255,255,220,${opacity})`
      ctx.fill()
    }

    animationFrameId = requestAnimationFrame(draw)
  }

  function handleResize() {
    resize()
    spawn()
  }

  resize()
  spawn()

  animationFrameId = requestAnimationFrame(draw)

  window.addEventListener('resize', handleResize)

  return function stopFireflies() {
    cancelAnimationFrame(animationFrameId)
    window.removeEventListener('resize', handleResize)
  }
}