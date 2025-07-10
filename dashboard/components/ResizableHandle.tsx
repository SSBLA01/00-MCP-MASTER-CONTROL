import React from 'react'

interface ResizableHandleProps {
  onMouseDown: (e: React.MouseEvent) => void
  orientation: 'horizontal' | 'vertical'
}

export function ResizableHandle({ onMouseDown, orientation }: ResizableHandleProps) {
  return (
    <div
      className={`
        ${orientation === 'horizontal' ? 'w-1 cursor-col-resize' : 'h-1 cursor-row-resize'}
        bg-gray-700 hover:bg-cyan-500/50 transition-colors
        relative group
      `}
      onMouseDown={onMouseDown}
    >
      <div
        className={`
          absolute ${orientation === 'horizontal' 
            ? 'inset-y-0 -left-1 -right-1' 
            : 'inset-x-0 -top-1 -bottom-1'
          }
        `}
      />
    </div>
  )
}