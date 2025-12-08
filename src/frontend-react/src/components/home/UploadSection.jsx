'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Camera, Clock, Save, Upload } from 'lucide-react';
import apiClient from '@/lib/api';

export default function UploadSection() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);

    // Get current time without rounding
    const getCurrentTime = () => {
        const now = new Date();

        // Convert to local timezone for datetime-local input
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const mins = String(now.getMinutes()).padStart(2, '0');

        return `${year}-${month}-${day}T${hours}:${mins}`;
    };

    const [mealTime, setMealTime] = useState(getCurrentTime());
    const [detectedDish, setDetectedDish] = useState('');
    const [ingredients, setIngredients] = useState([]);
    const [symptoms, setSymptoms] = useState({
        cramps: false,
        bloating: false,
        diarrhea: false,
        constipation: false,
        fullness: false,
        mucus: false,
    });
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [showSuccessModal, setShowSuccessModal] = useState(false);

    const handleFileSelect = async (e) => {
        const file = e.target.files?.[0];
        if (file) {
            setSelectedFile(file);
            const url = URL.createObjectURL(file);
            setPreviewUrl(url);

            // Analyze the photo
            await analyzePhoto(file);
        }
    };

    const analyzePhoto = async (file) => {
        setIsAnalyzing(true);
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await apiClient.post('/food-model/predict', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            console.log('API Response:', response.data);

            // Parse the response according to the backend API structure
            const dish = response.data.predicted_class || 'Unknown dish';
            const ingredients = response.data.ingredients || [];
            const confidence = response.data.confidence || 0;
            const fodmapLevel = response.data.fodmap_level || 'unknown';

            // Capitalize the dish name for better display
            const formattedDish = dish
                .split(' ')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');

            setDetectedDish(formattedDish);
            setIngredients(Array.isArray(ingredients) ? ingredients : []);
        } catch (error) {
            console.error('Error analyzing photo:', error);
            console.error('Error details:', error.response?.data);
            setDetectedDish('Error analyzing photo');
            setIngredients([]);
        } finally {
            setIsAnalyzing(false);
        }
    };

    const handleSymptomChange = (symptom) => {
        setSymptoms((prev) => ({
            ...prev,
            [symptom]: !prev[symptom],
        }));
    };

    const handleSaveEntry = async () => {
        setIsSaving(true);
        try {
            const selectedSymptoms = Object.keys(symptoms).filter((key) => symptoms[key]);

            // Get user_id from localStorage
            const userId = localStorage.getItem('tummyai_user_id') || 'default_user';

            // Convert local time to UTC for backend storage in ISO format
            const mealTimeUTC = new Date(mealTime).toISOString().slice(0, 19);

            // Upload photo to GCS
            if (selectedFile) {
                const photoFormData = new FormData();
                photoFormData.append('file', selectedFile);

                try {
                    await apiClient.post(
                        `/user-photo/${userId}/${encodeURIComponent(mealTimeUTC)}`,
                        photoFormData,
                        {
                            headers: {
                                'Content-Type': 'multipart/form-data',
                            },
                        }
                    );
                } catch (photoError) {
                    console.error('Error uploading photo:', photoError);
                    // Continue even if photo upload fails
                }
            }

            // Prepare meal data according to backend API structure
            const mealData = {
                date_time: mealTimeUTC,
                dish: detectedDish,
                ingredients: ingredients.join(', '), // Convert array to comma-separated string
                symptoms: selectedSymptoms.join(', '), // Convert array to comma-separated string
            };

            // Try to update meal history first
            try {
                await apiClient.put(`/meal-history/${userId}`, mealData);
            } catch (updateError) {
                // If update fails (404), create new meal history for this user
                if (updateError.response?.status === 404) {
                    // First create the meal history file
                    await apiClient.post(`/meal-history/${userId}`);
                    // Then add the meal entry
                    await apiClient.put(`/meal-history/${userId}`, mealData);
                } else {
                    throw updateError;
                }
            }

            // Update health report
            try {
                await apiClient.put(`/health-report/${userId}`, {
                    ingredients: ingredients.join(', '),
                    symptoms: selectedSymptoms.join(', '),
                });
            } catch (updateError) {
                // If update fails, create new report
                if (updateError.response?.status === 404) {
                    await apiClient.post(`/health-report/${userId}`);
                    await apiClient.put(`/health-report/${userId}`, {
                        ingredients: ingredients.join(', '),
                        symptoms: selectedSymptoms.join(', '),
                    });
                } else {
                    throw updateError;
                }
            }

            // Reset form
            setSelectedFile(null);
            setPreviewUrl(null);
            setDetectedDish('');
            setIngredients([]);
            setSymptoms({
                cramps: false,
                bloating: false,
                diarrhea: false,
                constipation: false,
                fullness: false,
                mucus: false,
            });
            setMealTime(getCurrentTime());

            setShowSuccessModal(true);
        } catch (error) {
            console.error('Error saving entry:', error);
            console.error('Error details:', error.response?.data);
            alert('Error saving entry.');
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="min-h-screen bg-background">
            <section className="py-16 px-4 sm:px-6 lg:px-8">
                <div className="max-w-7xl mx-auto">
                    <div className="mb-12">
                        <h1 className="text-4xl sm:text-5xl font-bold mb-4">
                            Track Your Meals
                        </h1>
                        <p className="text-lg text-muted-foreground">
                            Upload a photo of your meal and report symptoms to get personalized insights
                        </p>
                    </div>

                    {/* Meal Time and Save Entry Row */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                        {/* Meal Time Component */}
                        <Card className="p-6 lg:col-span-2">
                            <div className="flex items-center gap-4">
                                <Clock className="h-5 w-5 text-primary flex-shrink-0" />
                                <label className="text-sm font-medium whitespace-nowrap">
                                    Meal Time
                                </label>
                                <input
                                    type="datetime-local"
                                    value={mealTime}
                                    onChange={(e) => setMealTime(e.target.value)}
                                    className="flex-1 px-3 py-2 border rounded-md bg-background"
                                />
                            </div>
                        </Card>

                        {/* Save Entry Component */}
                        <Card className="p-6">
                            <div className="flex items-center justify-center h-full">
                                <Button
                                    onClick={handleSaveEntry}
                                    disabled={!selectedFile || isAnalyzing || isSaving}
                                    className="w-full"
                                    size="lg"
                                >
                                    <Save className="mr-2 h-4 w-4" />
                                    {isSaving ? 'Saving...' : 'Save Entry'}
                                </Button>
                            </div>
                        </Card>
                    </div>

                    {/* Two Column Grid */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Upload Meal Component */}
                        <Card className="p-6">
                            <h2 className="text-2xl font-bold mb-4">Upload Meal Photo</h2>

                            {/* Upload Button */}
                            <div className="mb-4">
                                <label className="block">
                                    <div className="border-2 border-dashed border-border rounded-lg p-6 text-center cursor-pointer hover:border-primary transition-colors">
                                        <Camera className="h-10 w-10 mx-auto mb-3 text-muted-foreground" />
                                        <p className="text-sm text-muted-foreground">
                                            Click to upload a photo of your meal
                                        </p>
                                        <input
                                            type="file"
                                            accept="image/*"
                                            onChange={handleFileSelect}
                                            className="hidden"
                                        />
                                    </div>
                                </label>
                            </div>

                            {/* Photo Preview */}
                            {previewUrl && (
                                <div className="mb-4">
                                    <img
                                        src={previewUrl}
                                        alt="Meal preview"
                                        className="w-full h-64 object-cover rounded-lg"
                                    />
                                </div>
                            )}

                            {/* Tips */}
                            <div className="bg-accent p-4 rounded-lg mb-4">
                                <h3 className="font-semibold mb-2">Tips for better photos:</h3>
                                <ul className="text-sm text-muted-foreground space-y-1">
                                    <li>• Capture the entire meal</li>
                                    <li>• Show every ingredient</li>
                                    <li>• Use good lighting</li>
                                </ul>
                            </div>

                            {/* Analysis Results */}
                            {isAnalyzing ? (
                                <div className="text-center py-4">
                                    <p className="text-muted-foreground">Analyzing photo...</p>
                                </div>
                            ) : (
                                detectedDish && (
                                    <div className="space-y-4">
                                        <div>
                                            <h3 className="font-semibold mb-2">Detected Dish:</h3>
                                            <p className="text-lg">{detectedDish}</p>
                                        </div>
                                        {ingredients.length > 0 && (
                                            <div>
                                                <h3 className="font-semibold mb-2">Ingredients:</h3>
                                                <div className="flex flex-wrap gap-2">
                                                    {ingredients.map((ingredient, index) => (
                                                        <span
                                                            key={index}
                                                            className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm"
                                                        >
                                                            {ingredient}
                                                        </span>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                )
                            )}
                        </Card>

                        {/* Report Symptoms Component */}
                        <Card className="p-6">
                            <h2 className="text-2xl font-bold mb-4">Report Symptoms</h2>
                            <p className="text-muted-foreground mb-6">
                                Which of the following symptoms did you experience after this meal? Select all that apply.
                            </p>

                            <div className="space-y-4">
                                {[
                                    { key: 'cramps', label: 'Abdominal pain or cramps' },
                                    { key: 'bloating', label: 'Excess gas and bloating' },
                                    { key: 'diarrhea', label: 'Diarrhea' },
                                    { key: 'constipation', label: 'Constipation' },
                                    { key: 'fullness', label: 'Sensation of incomplete evacuation' },
                                    { key: 'mucus', label: 'Mucus in stool' },
                                ].map((symptom) => (
                                    <label
                                        key={symptom.key}
                                        className="flex items-center gap-3 p-4 border rounded-lg cursor-pointer hover:bg-accent transition-colors"
                                    >
                                        <input
                                            type="checkbox"
                                            checked={symptoms[symptom.key]}
                                            onChange={() => handleSymptomChange(symptom.key)}
                                            className="w-4 h-4"
                                        />
                                        <span className="text-sm">{symptom.label}</span>
                                    </label>
                                ))}
                            </div>
                        </Card>
                    </div>
                </div>
            </section>

            {/* Success Modal */}
            {showSuccessModal && (
                <div
                    className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-in fade-in duration-200"
                    onClick={() => setShowSuccessModal(false)}
                >
                    <Card
                        className="p-8 max-w-sm mx-4 animate-in zoom-in-95 duration-200"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="text-center">
                            <h3 className="text-xl font-semibold">Entry saved!</h3>
                        </div>
                    </Card>
                </div>
            )}
        </div>
    );
}
