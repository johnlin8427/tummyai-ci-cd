'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';

export default function CheeseToggle({ onToggle, isActive }) {
    return (
        <Button
            variant="ghost"
            size="icon"
            onClick={onToggle}
            className={`w-9 h-9 hover:bg-accent ${isActive ? 'bg-accent' : ''}`}
        >
            <span
                className="text-xl"
                role="img"
                aria-label="cheese mode"
                style={{
                    filter: isActive ? 'none' : 'grayscale(100%)'
                }}
            >
                🧀
            </span>
            <span className="sr-only">Toggle cheese mode</span>
        </Button>
    );
}
