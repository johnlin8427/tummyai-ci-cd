'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { Home, Calendar, Info, Bot, Menu, X, User } from 'lucide-react';
import ThemeToggle from './ThemeToggle';
import CheeseToggle from './CheeseToggle';
import CheeseRain from './CheeseRain';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import apiClient from '@/lib/api';

export default function Header() {
    // Component States
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [showAccountModal, setShowAccountModal] = useState(false);
    const [currentUserId, setCurrentUserId] = useState('');
    const [newUserId, setNewUserId] = useState('');
    const [accountError, setAccountError] = useState('');
    const [cheeseMode, setCheeseMode] = useState(false);
    const pathname = usePathname();

    useEffect(() => {
        // Load user_id from localStorage or use default
        const storedUserId = localStorage.getItem('tummyai_user_id') || 'default_user';
        setCurrentUserId(storedUserId);
    }, []);

    const handleAccountChange = async () => {
        if (newUserId.trim()) {
            const userId = newUserId.trim();
            try {
                // Check if user exists
                const response = await apiClient.get('/user-list');
                const users = response.data.user_list || [];

                if (!users.includes(userId)) {
                    setAccountError('Account does not exist. Please use Create Account instead.');
                    return;
                }

                // User exists, switch to it
                localStorage.setItem('tummyai_user_id', userId);
                setCurrentUserId(userId);
                setNewUserId('');
                setAccountError('');
                setShowAccountModal(false);
                // Reload the page to fetch data for new user
                window.location.reload();
            } catch (error) {
                console.error('Error switching account:', error);
                setAccountError('Error checking account. Please try again.');
            }
        }
    };

    const handleCreateAccount = async () => {
        if (newUserId.trim()) {
            const userId = newUserId.trim();
            try {
                // Check if user already exists
                const response = await apiClient.get('/user-list');
                const users = response.data.user_list || [];

                if (users.includes(userId)) {
                    setAccountError('Account already exists. Please use Switch Account instead.');
                    return;
                }

                // Create new user in user list
                await apiClient.put(`/user-list/${encodeURIComponent(userId)}`);

                // Create meal history for the new user
                try {
                    await apiClient.post(`/meal-history/${userId}`);
                } catch (mealHistoryError) {
                    // Log but continue if meal history already exists
                    console.log('Meal history creation:', mealHistoryError);
                }

                // Create health report for the new user
                try {
                    await apiClient.post(`/health-report/${userId}`);
                } catch (healthReportError) {
                    // Log but continue if health report already exists
                    console.log('Health report creation:', healthReportError);
                }

                // Set as current user
                localStorage.setItem('tummyai_user_id', userId);
                setCurrentUserId(userId);
                setNewUserId('');
                setAccountError('');
                setShowAccountModal(false);
                // Reload the page to fetch data for new user
                window.location.reload();
            } catch (error) {
                console.error('Error creating account:', error);
                setAccountError('Error creating account. Please try again.');
            }
        }
    };

    // Add your navigation items here
    const navItems = [
        { name: 'Home', path: '/', icon: <Home className="h-5 w-5" /> },
        { name: 'Meal History', path: '/history', icon: <Calendar className="h-5 w-5" /> },
        { name: 'Health Report', path: '/report', icon: <Info className="h-5 w-5" /> }
    ];

    // UI View
    return (
        <>
            <header className="header-wrapper">
                <div className="header-container">
                    <div className="header-content">
                        <Link href="/" className="header-logo">
                            <Image
                                src="/assets/logo.svg"
                                alt="TummyAI Logo"
                                width={32}
                                height={32}
                                className="w-8 h-8"
                            />
                            <h1 className="text-xl font-bold">TummyAI</h1>
                        </Link>

                        <nav className="nav-desktop">
                            {navItems.map((item) => (
                                <Link
                                    key={item.name}
                                    href={item.path}
                                    className={`nav-link ${pathname === item.path ? 'nav-link-active' : ''}`}
                                >
                                    <div className="nav-icon-wrapper">{item.icon}</div>
                                    <span className="nav-text">{item.name}</span>
                                </Link>
                            ))}
                        </nav>

                        <div className="flex items-center gap-2">
                            <button
                                className="p-2 rounded-md hover:bg-accent transition-colors hidden md:flex"
                                onClick={() => setShowAccountModal(true)}
                                aria-label="Account"
                            >
                                <User className="h-5 w-5" />
                            </button>
                            <ThemeToggle />
                            <CheeseToggle onToggle={() => setCheeseMode(!cheeseMode)} isActive={cheeseMode} />
                            <button
                                className="mobile-menu-button"
                                onClick={() => setIsMenuOpen(!isMenuOpen)}
                                aria-label="Toggle menu"
                            >
                                {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Mobile Menu */}
                {isMenuOpen && (
                    <div className="mobile-menu translate-y-0">
                        <nav className="px-4 py-2 space-y-1">
                            {navItems.map((item) => (
                                <Link
                                    key={item.name}
                                    href={item.path}
                                    className={`flex items-center gap-3 px-3 py-2 rounded-md text-muted-foreground hover:text-foreground hover:bg-accent transition-all ${
                                        pathname === item.path ? 'bg-accent text-foreground font-medium' : ''
                                    }`}
                                    onClick={() => setIsMenuOpen(false)}
                                >
                                    {item.icon}
                                    <span>{item.name}</span>
                                </Link>
                            ))}
                        </nav>
                    </div>
                )}
            </header>

            {/* Account Modal */}
            {showAccountModal && (
                <div
                    className="fixed inset-0 bg-black/50 flex items-center justify-center z-[9999] p-4"
                    onClick={() => {
                        setShowAccountModal(false);
                        setAccountError('');
                    }}
                >
                    <Card
                        className="p-6 max-w-md w-full"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <h2 className="text-2xl font-bold mb-4">Account</h2>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium mb-2">
                                    Current User ID
                                </label>
                                <div className="p-3 bg-muted rounded-md">
                                    {currentUserId}
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium mb-2">
                                    Enter User ID
                                </label>
                                <input
                                    type="text"
                                    value={newUserId}
                                    onChange={(e) => {
                                        setNewUserId(e.target.value);
                                        setAccountError('');
                                    }}
                                    placeholder="Enter user ID"
                                    className="w-full px-3 py-2 border rounded-md bg-background"
                                    onKeyPress={(e) => e.key === 'Enter' && handleAccountChange()}
                                />
                                {accountError && (
                                    <p className="text-sm text-destructive mt-2">
                                        {accountError}
                                    </p>
                                )}
                            </div>
                            <div className="flex gap-2">
                                <Button
                                    onClick={handleAccountChange}
                                    disabled={!newUserId.trim()}
                                    className="flex-1"
                                >
                                    Switch Account
                                </Button>
                                <Button
                                    onClick={handleCreateAccount}
                                    disabled={!newUserId.trim()}
                                    variant="secondary"
                                    className="flex-1"
                                >
                                    Create Account
                                </Button>
                                <Button
                                    onClick={() => {
                                        setShowAccountModal(false);
                                        setAccountError('');
                                    }}
                                    variant="outline"
                                    className="flex-1"
                                >
                                    Cancel
                                </Button>
                            </div>
                        </div>
                    </Card>
                </div>
            )}

            {isMenuOpen && <div className="mobile-menu-overlay" onClick={() => setIsMenuOpen(false)} />}

            {cheeseMode && <CheeseRain />}
        </>
    );
}
