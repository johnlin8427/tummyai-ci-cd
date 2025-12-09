'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { LayoutGrid, List, X } from 'lucide-react';
import apiClient from '@/lib/api';

export default function RecentMealsSection() {
    const [meals, setMeals] = useState([]);
    const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
    const [selectedMeal, setSelectedMeal] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        fetchMealHistory();
    }, []);

    const fetchMealHistory = async () => {
        setIsLoading(true);
        try {
            // Get user_id from localStorage
            const userId = localStorage.getItem('tummyai_user_id') || 'default_user';
            const response = await apiClient.get(`/meal-history/${userId}`);

            // Parse the response and format for display with placeholder photos initially
            const formattedMeals = (response.data || []).map((meal, index) => {
                // Parse comma-separated strings into arrays
                const ingredients = meal.ingredients ? meal.ingredients.split(', ').filter(x => x) : [];
                const ingredientsFodmapHigh = meal.ingredients_fodmap_high ? meal.ingredients_fodmap_high.split(', ').filter(x => x) : [];
                const ingredientsFodmapLow = meal.ingredients_fodmap_low ? meal.ingredients_fodmap_low.split(', ').filter(x => x) : [];
                const ingredientsFodmapNone = meal.ingredients_fodmap_none ? meal.ingredients_fodmap_none.split(', ').filter(x => x) : [];

                return {
                    id: index + 1,
                    timestamp: meal.date_time,
                    photo: null,
                    dish: meal.dish || 'Meal',
                    dishFodmap: meal.dish_fodmap || 'unknown',
                    ingredients: ingredients,
                    ingredientsFodmapHigh: ingredientsFodmapHigh,
                    ingredientsFodmapLow: ingredientsFodmapLow,
                    ingredientsFodmapNone: ingredientsFodmapNone,
                    symptoms: meal.symptoms ? meal.symptoms.split(', ').filter(s => s) : [],
                };
            }).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)); // Sort by newest first

            // Set meals data first so UI renders immediately
            setMeals(formattedMeals);
            setIsLoading(false);

            // Fetch photos asynchronously in reverse chronological order
            for (const meal of formattedMeals) {
                try {
                    const photoResponse = await apiClient.get(
                        `/user-photo/${userId}/${meal.timestamp}`,
                        { responseType: 'blob' }
                    );
                    const photoUrl = URL.createObjectURL(photoResponse.data);

                    // Update the specific meal with the photo
                    setMeals(prevMeals => {
                        const updatedMeals = [...prevMeals];
                        const mealIndex = updatedMeals.findIndex(m => m.timestamp === meal.timestamp);
                        if (mealIndex !== -1) {
                            updatedMeals[mealIndex].photo = photoUrl;
                        }
                        return updatedMeals;
                    });
                } catch (photoError) {
                    // Keep placeholder if photo not found
                    console.log('Photo not found for meal:', meal.timestamp);
                }
            }
        } catch (error) {
            console.error('Error fetching meal history:', error);
            setIsLoading(false);
            // Use mock data for development
            setMeals([
                {
                    id: 1,
                    timestamp: '2025-12-07T12:30:00',
                    photo: null,
                    dish: 'Grilled Chicken Salad',
                    ingredients: ['Chicken', 'Lettuce', 'Tomatoes', 'Cucumber', 'Olive Oil'],
                    symptoms: ['bloating'],
                },
                {
                    id: 2,
                    timestamp: '2025-12-06T18:45:00',
                    photo: null,
                    dish: 'Pasta Carbonara',
                    ingredients: ['Pasta', 'Eggs', 'Bacon', 'Parmesan', 'Black Pepper'],
                    symptoms: ['cramps', 'diarrhea'],
                },
            ]);
        }
    };

    const formatDate = (timestamp) => {
        // Backend stores in UTC, convert to local time for display
        const date = new Date(timestamp + 'Z'); // Add Z to indicate UTC
        return date.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            hour12: true,
        });
    };

    const getSymptomLabel = (symptomKey) => {
        const labels = {
            cramping: 'abdominal pain or cramps',
            cramps: 'abdominal pain or cramps',
            bloating: 'excess gas and bloating',
            diarrhea: 'diarrhea',
            constipation: 'constipation',
            fullness: 'sensation of incomplete evacuation',
            unfinished: 'sensation of incomplete evacuation',
            mucus: 'mucus in stool',
            nausea: 'nausea',
        };
        return labels[symptomKey] || symptomKey.toLowerCase();
    };

    const MealCard = ({ meal, onClick }) => (
        <Card
            className="p-4 cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => onClick(meal)}
        >
            <div className="aspect-video mb-3 bg-muted rounded-lg overflow-hidden">
                {meal.photo ? (
                    <img
                        src={meal.photo}
                        alt={meal.dish}
                        className="w-full h-full object-cover"
                    />
                ) : (
                    <div className="w-full h-full bg-gray-300 dark:bg-gray-700" />
                )}
            </div>
            <div className="space-y-2">
                <div className="text-sm text-muted-foreground">
                    {formatDate(meal.timestamp)}
                </div>
                <h3 className="font-semibold text-xl">{meal.dish.toLowerCase()}</h3>
                {meal.dishFodmap && (
                    <div>
                        <div className="text-xs font-semibold text-muted-foreground mb-1">Overall FODMAP Level:</div>
                        <span
                            className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${
                                meal.dishFodmap === 'high' || meal.dishFodmap === 'unknown'
                                    ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                                    : meal.dishFodmap === 'low' || meal.dishFodmap === 'moderate'
                                    ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                                    : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            }`}
                        >
                            {meal.dishFodmap}
                        </span>
                    </div>
                )}
                <div>
                    <div className="text-xs font-semibold text-muted-foreground mb-1">Ingredients:</div>
                    <div className="flex flex-wrap gap-1">
                        {meal.ingredientsFodmapHigh.map((ingredient, index) => (
                            <span
                                key={`high-${index}`}
                                className="px-2 py-0.5 bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 rounded-full text-xs font-medium"
                            >
                                {ingredient}
                            </span>
                        ))}
                        {meal.ingredientsFodmapLow.map((ingredient, index) => (
                            <span
                                key={`low-${index}`}
                                className="px-2 py-0.5 bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200 rounded-full text-xs font-medium"
                            >
                                {ingredient}
                            </span>
                        ))}
                        {meal.ingredientsFodmapNone.map((ingredient, index) => (
                            <span
                                key={`none-${index}`}
                                className="px-2 py-0.5 bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 rounded-full text-xs font-medium"
                            >
                                {ingredient}
                            </span>
                        ))}
                    </div>
                </div>
                {meal.symptoms.length > 0 && (
                    <div>
                        <div className="text-xs font-semibold text-muted-foreground mb-1">Symptoms:</div>
                        <div className="flex flex-wrap gap-1">
                            {meal.symptoms.map((symptom, index) => (
                                <span
                                    key={index}
                                    className="px-2 py-0.5 bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 rounded-full text-xs font-medium"
                                >
                                    {getSymptomLabel(symptom)}
                                </span>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </Card>
    );

    const MealListItem = ({ meal, onClick }) => (
        <Card
            className="p-4 cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => onClick(meal)}
        >
            <div className="flex gap-4">
                <div className="w-32 h-32 flex-shrink-0 bg-muted rounded-lg overflow-hidden">
                    {meal.photo ? (
                        <img
                            src={meal.photo}
                            alt={meal.dish}
                            className="w-full h-full object-cover"
                        />
                    ) : (
                        <div className="w-full h-full bg-gray-300 dark:bg-gray-700" />
                    )}
                </div>
                <div className="flex-1 space-y-2">
                    <div className="text-sm text-muted-foreground">
                        {formatDate(meal.timestamp)}
                    </div>
                    <h3 className="font-semibold text-xl">{meal.dish.toLowerCase()}</h3>
                    {meal.dishFodmap && (
                        <div>
                            <div className="text-xs font-semibold text-muted-foreground mb-1">Overall FODMAP Level:</div>
                            <span
                                className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${
                                    meal.dishFodmap === 'high' || meal.dishFodmap === 'unknown'
                                        ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                                        : meal.dishFodmap === 'low' || meal.dishFodmap === 'moderate'
                                        ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                                        : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                                }`}
                            >
                                {meal.dishFodmap}
                            </span>
                        </div>
                    )}
                    <div>
                        <div className="text-xs font-semibold text-muted-foreground mb-1">Ingredients:</div>
                        <div className="flex flex-wrap gap-1">
                            {meal.ingredientsFodmapHigh.map((ingredient, index) => (
                                <span
                                    key={`high-${index}`}
                                    className="px-2 py-0.5 bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 rounded-full text-xs font-medium"
                                >
                                    {ingredient}
                                </span>
                            ))}
                            {meal.ingredientsFodmapLow.map((ingredient, index) => (
                                <span
                                    key={`low-${index}`}
                                    className="px-2 py-0.5 bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200 rounded-full text-xs font-medium"
                                >
                                    {ingredient}
                                </span>
                            ))}
                            {meal.ingredientsFodmapNone.map((ingredient, index) => (
                                <span
                                    key={`none-${index}`}
                                    className="px-2 py-0.5 bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 rounded-full text-xs font-medium"
                                >
                                    {ingredient}
                                </span>
                            ))}
                        </div>
                    </div>
                    {meal.symptoms.length > 0 && (
                        <div>
                            <div className="text-xs font-semibold text-muted-foreground mb-1">Symptoms:</div>
                            <div className="flex flex-wrap gap-1">
                                {meal.symptoms.map((symptom, index) => (
                                    <span
                                        key={index}
                                        className="px-2 py-0.5 bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 rounded-full text-xs font-medium"
                                    >
                                        {getSymptomLabel(symptom)}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </Card>
    );

    const MealDetailModal = ({ meal, onClose }) => {
        if (!meal) return null;

        return (
            <div
                className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
                onClick={onClose}
            >
                <Card
                    className="w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6"
                    onClick={(e) => e.stopPropagation()}
                >
                    <div className="space-y-4">
                        <div className="aspect-video bg-muted rounded-lg overflow-hidden">
                            {meal.photo ? (
                                <img
                                    src={meal.photo}
                                    alt={meal.dish}
                                    className="w-full h-full object-cover"
                                />
                            ) : (
                                <div className="w-full h-full bg-gray-300 dark:bg-gray-700" />
                            )}
                        </div>

                        <div>
                            <h3 className="font-semibold mb-2">Time & Date</h3>
                            <p className="text-muted-foreground">{formatDate(meal.timestamp)}</p>
                        </div>

                        <div>
                            <h3 className="font-semibold mb-2">Dish</h3>
                            <p className="text-muted-foreground">{meal.dish.toLowerCase()}</p>
                        </div>

                        {meal.dishFodmap && (
                            <div>
                                <h3 className="font-semibold mb-2">Overall FODMAP Level</h3>
                                <span
                                    className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${
                                        meal.dishFodmap === 'high' || meal.dishFodmap === 'unknown'
                                            ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                                            : meal.dishFodmap === 'low' || meal.dishFodmap === 'moderate'
                                            ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                                            : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                                    }`}
                                >
                                    {meal.dishFodmap}
                                </span>
                            </div>
                        )}

                        <div>
                            <h3 className="font-semibold mb-2">Ingredients</h3>
                            <div className="flex flex-wrap gap-2">
                                {meal.ingredientsFodmapHigh.map((ingredient, index) => (
                                    <span
                                        key={`high-${index}`}
                                        className="px-3 py-1 bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 rounded-full font-medium"
                                    >
                                        {ingredient}
                                    </span>
                                ))}
                                {meal.ingredientsFodmapLow.map((ingredient, index) => (
                                    <span
                                        key={`low-${index}`}
                                        className="px-3 py-1 bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200 rounded-full font-medium"
                                    >
                                        {ingredient}
                                    </span>
                                ))}
                                {meal.ingredientsFodmapNone.map((ingredient, index) => (
                                    <span
                                        key={`none-${index}`}
                                        className="px-3 py-1 bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 rounded-full font-medium"
                                    >
                                        {ingredient}
                                    </span>
                                ))}
                            </div>
                        </div>

                        <div>
                            <h3 className="font-semibold mb-2">Symptoms</h3>
                            {meal.symptoms.length > 0 ? (
                                <div className="flex flex-wrap gap-2">
                                    {meal.symptoms.map((symptom, index) => (
                                        <span
                                            key={index}
                                            className="px-3 py-1 bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 rounded-full font-medium"
                                        >
                                            {getSymptomLabel(symptom)}
                                        </span>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-muted-foreground">No symptoms reported</p>
                            )}
                        </div>
                    </div>
                </Card>
            </div>
        );
    };

    return (
        <div className="min-h-screen bg-background">
            <section className="py-16 px-4 sm:px-6 lg:px-8">
                <div className="max-w-7xl mx-auto">
                    <div className="mb-12">
                        <div className="flex justify-between items-start mb-4">
                            <div>
                                <h1 className="text-4xl sm:text-5xl font-bold mb-4">Meal History</h1>
                                <p className="text-lg text-muted-foreground">
                                    View your recent meals and symptoms
                                </p>
                            </div>
                            <div className="flex gap-2">
                                <Button
                                    variant={viewMode === 'grid' ? 'default' : 'outline'}
                                    size="icon"
                                    onClick={() => setViewMode('grid')}
                                >
                                    <LayoutGrid className="h-4 w-4" />
                                </Button>
                                <Button
                                    variant={viewMode === 'list' ? 'default' : 'outline'}
                                    size="icon"
                                    onClick={() => setViewMode('list')}
                                >
                                    <List className="h-4 w-4" />
                                </Button>
                            </div>
                        </div>
                    </div>

                    {isLoading ? (
                        <div className="text-center py-12">
                            <p className="text-muted-foreground">Loading meal history...</p>
                        </div>
                    ) : meals.length === 0 ? (
                        <div className="text-center py-12">
                            <p className="text-muted-foreground">
                                No meals recorded yet. Start by uploading your first meal!
                            </p>
                        </div>
                    ) : (
                        <div
                            className={
                                viewMode === 'grid'
                                    ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
                                    : 'space-y-4'
                            }
                        >
                            {meals.map((meal) =>
                                viewMode === 'grid' ? (
                                    <MealCard
                                        key={meal.id}
                                        meal={meal}
                                        onClick={setSelectedMeal}
                                    />
                                ) : (
                                    <MealListItem
                                        key={meal.id}
                                        meal={meal}
                                        onClick={setSelectedMeal}
                                    />
                                )
                            )}
                        </div>
                    )}
                </div>
            </section>

            {selectedMeal && (
                <MealDetailModal
                    meal={selectedMeal}
                    onClose={() => setSelectedMeal(null)}
                />
            )}
        </div>
    );
}
