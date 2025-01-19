export default function BaseballScoreboard() {
  return (
    <div className="max-w-md rounded-lg border bg-white p-4 shadow-sm">
      <div className="mb-4">
        <div className="mb-2 text-sm font-medium text-gray-500">FINAL</div>
        <div className="text-xs text-gray-500">Free Game of the Day</div>
      </div>

      <div className="mb-6 grid grid-cols-[1fr,auto,auto,auto] items-center gap-4">
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <div className="h-6 w-6 rounded bg-[#092C5C] text-center text-sm leading-6 text-white">TB</div>
            <div className="flex items-baseline gap-2">
              <span className="font-medium">Rays</span>
              <span className="text-sm text-gray-500">11 - 16</span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="h-6 w-6">
              <img
                src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-FdQGiin0vrFh2T0INxjkaOYeOJSNnG.png"
                alt="Phillies logo"
                className="h-6 w-6 object-contain"
              />
            </div>
            <div className="flex items-baseline gap-2">
              <span className="font-medium">Phillies</span>
              <span className="text-sm text-gray-500">9 - 15</span>
            </div>
          </div>
        </div>

        <div className="text-center font-medium">
          <div className="mb-4">6</div>
          <div>3</div>
        </div>

        <div className="text-center font-medium">
          <div className="mb-4">9</div>
          <div>7</div>
        </div>

        <div className="text-center font-medium">
          <div className="mb-4">1</div>
          <div>2</div>
        </div>
      </div>

      <div className="mb-6 grid grid-cols-2 gap-8">
        <div className="flex gap-3">
          <div className="h-10 w-10 overflow-hidden rounded-full bg-gray-100">
            <img
              src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-FdQGiin0vrFh2T0INxjkaOYeOJSNnG.png"
              alt="Fairbanks"
              className="h-full w-full object-cover"
            />
          </div>
          <div>
            <div className="text-sm">W: Fairbanks</div>
            <div className="text-sm text-gray-500">2 - 0 | 0.00 ERA</div>
          </div>
        </div>
        <div className="flex gap-3">
          <div className="h-10 w-10 overflow-hidden rounded-full bg-gray-100">
            <img
              src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-FdQGiin0vrFh2T0INxjkaOYeOJSNnG.png"
              alt="Contreras"
              className="h-full w-full object-cover"
            />
          </div>
          <div>
            <div className="text-sm">L: Contreras</div>
            <div className="text-sm text-gray-500">0 - 1 | 18.00 ERA</div>
          </div>
        </div>
      </div>

      <div className="flex gap-6 border-t pt-4">
        <button className="text-sm font-medium text-blue-600">Wrap</button>
        <button className="text-sm font-medium text-gray-600">Box</button>
        <button className="text-sm font-medium text-gray-600">Story</button>
      </div>
    </div>
  )
}