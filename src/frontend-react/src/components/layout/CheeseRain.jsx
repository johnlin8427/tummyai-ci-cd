'use client';

import { useEffect, useState } from 'react';

export default function CheeseRain() {
    const [cheeses, setCheeses] = useState([]);

    useEffect(() => {
        // Generate falling cheese icons
        const generateCheese = () => {
            const id = Date.now() + Math.random();
            const left = Math.random() * 100;
            const duration = 3 + Math.random() * 4; // 3-7 seconds
            const delay = Math.random() * 2;
            const size = 20 + Math.random() * 20; // 20-40px
            const rotation = Math.random() * 360;

            return {
                id,
                left: `${left}%`,
                duration: `${duration}s`,
                delay: `${delay}s`,
                size: `${size}px`,
                rotation: `${rotation}deg`,
            };
        };

        // Create initial batch of cheese
        const initialCheeses = Array.from({ length: 15 }, () => generateCheese());
        setCheeses(initialCheeses);

        // Continuously add new cheese
        const interval = setInterval(() => {
            setCheeses(prev => {
                // Remove old cheeses and add new ones
                const newCheese = generateCheese();
                return [...prev.slice(-20), newCheese]; // Keep max 20 cheeses
            });
        }, 400);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="fixed inset-0 pointer-events-none z-[9999] overflow-hidden">
            {cheeses.map((cheese) => (
                <div
                    key={cheese.id}
                    className="absolute animate-fall"
                    style={{
                        left: cheese.left,
                        top: '-50px',
                        fontSize: cheese.size,
                        animationDuration: cheese.duration,
                        animationDelay: cheese.delay,
                        transform: `rotate(${cheese.rotation})`,
                    }}
                >
                    🧀
                </div>
            ))}
            <style jsx>{`
                @keyframes fall {
                    0% {
                        transform: translateY(0) rotate(0deg);
                        opacity: 1;
                    }
                    95% {
                        opacity: 1;
                    }
                    100% {
                        transform: translateY(calc(100vh + 100px)) rotate(720deg);
                        opacity: 0;
                    }
                }
                .animate-fall {
                    animation: fall linear forwards;
                }
            `}</style>
        </div>
    );
}
