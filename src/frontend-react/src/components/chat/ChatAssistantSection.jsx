'use client';

import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Send, Bot, User } from 'lucide-react';
import apiClient from '@/lib/api';

export default function ChatAssistantSection() {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content:
                "Hello! I'm your TummyAI assistant. I can help you with questions about your gut health, meal tracking, and managing IBS symptoms. How can I help you today?",
        },
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');

        // Add user message to chat
        setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            // Call chat API
            const response = await apiClient.post('/chat', {
                message: userMessage,
                history: messages,
            });

            // Add assistant response
            setMessages((prev) => [
                ...prev,
                { role: 'assistant', content: response.data.message },
            ]);
        } catch (error) {
            console.error('Error sending message:', error);
            // Mock response for development
            setTimeout(() => {
                setMessages((prev) => [
                    ...prev,
                    {
                        role: 'assistant',
                        content:
                            "I'm here to help! Based on your meal history, I can provide insights about foods that may trigger your symptoms. For more specific advice, please consult with a healthcare professional.",
                    },
                ]);
                setIsLoading(false);
            }, 1000);
            return;
        } finally {
            setIsLoading(false);
        }
    };

    const suggestedQuestions = [
        'What foods should I avoid with IBS?',
        'How can I reduce bloating?',
        'What are common IBS triggers?',
        'Tell me about the low FODMAP diet',
    ];

    const handleSuggestedQuestion = (question) => {
        setInput(question);
    };

    return (
        <div className="min-h-screen bg-background">
            <section className="py-16 px-4 sm:px-6 lg:px-8">
                <div className="max-w-4xl mx-auto">
                    <div className="mb-12">
                        <h1 className="text-4xl sm:text-5xl font-bold mb-4">Chat Assistant</h1>
                        <p className="text-lg text-muted-foreground">
                            Ask questions about your gut health and get personalized guidance
                        </p>
                    </div>

                    <Card className="flex flex-col h-[600px]">
                        {/* Chat Messages */}
                        <div className="flex-1 overflow-y-auto p-6 space-y-4">
                            {messages.map((message, index) => (
                                <div
                                    key={index}
                                    className={`flex items-start gap-3 ${
                                        message.role === 'user' ? 'flex-row-reverse' : ''
                                    }`}
                                >
                                    <div
                                        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                                            message.role === 'user'
                                                ? 'bg-primary text-primary-foreground'
                                                : 'bg-muted'
                                        }`}
                                    >
                                        {message.role === 'user' ? (
                                            <User className="h-4 w-4" />
                                        ) : (
                                            <Bot className="h-4 w-4" />
                                        )}
                                    </div>
                                    <div
                                        className={`flex-1 max-w-[80%] p-4 rounded-lg ${
                                            message.role === 'user'
                                                ? 'bg-primary text-primary-foreground'
                                                : 'bg-muted'
                                        }`}
                                    >
                                        <p className="text-sm whitespace-pre-wrap">
                                            {message.content}
                                        </p>
                                    </div>
                                </div>
                            ))}
                            {isLoading && (
                                <div className="flex items-start gap-3">
                                    <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-muted">
                                        <Bot className="h-4 w-4" />
                                    </div>
                                    <div className="flex-1 max-w-[80%] p-4 rounded-lg bg-muted">
                                        <div className="flex gap-1">
                                            <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                                            <div
                                                className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                                                style={{ animationDelay: '0.1s' }}
                                            ></div>
                                            <div
                                                className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                                                style={{ animationDelay: '0.2s' }}
                                            ></div>
                                        </div>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Suggested Questions */}
                        {messages.length === 1 && (
                            <div className="px-6 pb-4">
                                <p className="text-sm text-muted-foreground mb-2">
                                    Suggested questions:
                                </p>
                                <div className="flex flex-wrap gap-2">
                                    {suggestedQuestions.map((question, index) => (
                                        <Button
                                            key={index}
                                            variant="outline"
                                            size="sm"
                                            onClick={() => handleSuggestedQuestion(question)}
                                            className="text-xs"
                                        >
                                            {question}
                                        </Button>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Input Form */}
                        <div className="border-t p-4">
                            <form onSubmit={handleSendMessage} className="flex gap-2">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    placeholder="Ask a question about your gut health..."
                                    className="flex-1 px-4 py-2 border rounded-lg bg-background focus:outline-none focus:ring-2 focus:ring-primary"
                                    disabled={isLoading}
                                />
                                <Button
                                    type="submit"
                                    disabled={!input.trim() || isLoading}
                                    size="icon"
                                >
                                    <Send className="h-4 w-4" />
                                </Button>
                            </form>
                            <p className="text-xs text-muted-foreground mt-2">
                                This assistant provides general information. Always consult a
                                healthcare professional for medical advice.
                            </p>
                        </div>
                    </Card>
                </div>
            </section>
        </div>
    );
}
