'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { AlertTriangle, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import apiClient from '@/lib/api';

export default function HealthReportSection() {
    const [healthData, setHealthData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [recommendations, setRecommendations] = useState(null);
    const [isLoadingRecommendations, setIsLoadingRecommendations] = useState(false);

    useEffect(() => {
        fetchHealthReport();
    }, []);

    const fetchHealthReport = async () => {
        setIsLoading(true);
        try {
            const userId = localStorage.getItem('tummyai_user_id') || 'default_user';
            const [healthResponse, mealHistoryResponse] = await Promise.all([
                apiClient.get(`/health-report/${userId}`),
                apiClient.get(`/meal-history/${userId}`)
            ]);

            // Transform the API response into the expected format
            const rawData = healthResponse.data || [];
            const mealHistory = mealHistoryResponse.data || [];

            // Process foods to watch - group by ingredient
            const ingredientMap = {};
            rawData.forEach(item => {
                if (!ingredientMap[item.ingredient]) {
                    ingredientMap[item.ingredient] = {
                        name: item.ingredient.toLowerCase(),
                        symptoms: [],
                        minPValueAdj: 1,
                        minPValue: 1,
                        maxOddsRatio: 0,
                    };
                }

                // Only consider items with odds_ratio > 1 or null AND p_value < 0.2
                if ((item.odds_ratio === null || item.odds_ratio > 1) && item.p_value !== null && item.p_value < 0.2) {
                    ingredientMap[item.ingredient].symptoms.push({
                        symptom: item.symptom,
                        oddsRatio: item.odds_ratio,
                        pValue: item.p_value,
                        pValueAdj: item.p_value_adj,
                    });

                    if (item.odds_ratio && item.odds_ratio > ingredientMap[item.ingredient].maxOddsRatio) {
                        ingredientMap[item.ingredient].maxOddsRatio = item.odds_ratio;
                    }

                    // Track minimum p-values
                    if (item.p_value_adj !== null && item.p_value_adj < ingredientMap[item.ingredient].minPValueAdj) {
                        ingredientMap[item.ingredient].minPValueAdj = item.p_value_adj;
                    }
                    if (item.p_value !== null && item.p_value < ingredientMap[item.ingredient].minPValue) {
                        ingredientMap[item.ingredient].minPValue = item.p_value;
                    }
                }
            });

            // Convert to foods to watch array
            const foodsToWatch = Object.values(ingredientMap)
                .filter(food => food.symptoms.length > 0)
                .map(food => {
                    // Determine risk level based on p-values
                    let riskLevel = 'low';

                    // High risk: p_value_adj < 0.05
                    if (food.minPValueAdj < 0.05) {
                        riskLevel = 'high';
                    }
                    // Medium risk: p_value between 0.05 and 0.1
                    else if (food.minPValue >= 0.05 && food.minPValue < 0.1) {
                        riskLevel = 'medium';
                    }
                    // Low risk: p_value between 0.1 and 0.2
                    else if (food.minPValue >= 0.1 && food.minPValue < 0.2) {
                        riskLevel = 'low';
                    }
                    // No significant risk if p_value >= 0.2
                    else {
                        return null; // Filter out later
                    }

                    return {
                        name: food.name,
                        occurrences: food.symptoms.length,
                        symptomsTriggered: [...new Set(food.symptoms.map(s => s.symptom))],
                        riskLevel: riskLevel,
                    };
                })
                .filter(food => food !== null) // Remove items with no significant risk
                .sort((a, b) => {
                    // Sort by risk level and then by occurrences
                    const riskOrder = { high: 3, medium: 2, low: 1 };
                    if (riskOrder[b.riskLevel] !== riskOrder[a.riskLevel]) {
                        return riskOrder[b.riskLevel] - riskOrder[a.riskLevel];
                    }
                    return b.occurrences - a.occurrences;
                });

            // Process symptom trends - calculate this week vs last week
            const now = new Date();
            const thisWeekStart = new Date(now);
            thisWeekStart.setDate(now.getDate() - 7);
            const lastWeekStart = new Date(now);
            lastWeekStart.setDate(now.getDate() - 14);

            const symptomCounts = {};

            mealHistory.forEach(meal => {
                if (!meal.symptoms || !meal.date_time) return;

                const mealDate = new Date(meal.date_time);
                const symptoms = meal.symptoms.split(', ').filter(s => s);

                symptoms.forEach(symptom => {
                    if (!symptomCounts[symptom]) {
                        symptomCounts[symptom] = {
                            thisWeek: 0,
                            lastWeek: 0
                        };
                    }

                    if (mealDate >= thisWeekStart) {
                        symptomCounts[symptom].thisWeek++;
                    } else if (mealDate >= lastWeekStart && mealDate < thisWeekStart) {
                        symptomCounts[symptom].lastWeek++;
                    }
                });
            });

            // Convert to symptom trends array
            const symptomOrder = ['cramps', 'bloating', 'diarrhea', 'constipation', 'fullness', 'mucus'];
            let symptomTrends = Object.entries(symptomCounts)
                .map(([symptom, counts]) => {
                    let trend = 'stable';
                    let change = 0;

                    if (counts.lastWeek === 0 && counts.thisWeek > 0) {
                        trend = 'increasing';
                        change = counts.thisWeek;
                    } else if (counts.thisWeek > counts.lastWeek) {
                        trend = 'increasing';
                        change = counts.thisWeek - counts.lastWeek;
                    } else if (counts.thisWeek < counts.lastWeek) {
                        trend = 'decreasing';
                        change = counts.lastWeek - counts.thisWeek;
                    }

                    return {
                        symptomKey: symptom,
                        symptom: getSymptomLabel(symptom),
                        trend: trend,
                        thisWeekCount: counts.thisWeek,
                        lastWeekCount: counts.lastWeek,
                        change: change,
                    };
                })
                .filter(item => item.thisWeekCount > 0 || item.lastWeekCount > 0)
                .sort((a, b) => {
                    // Sort by questionnaire order
                    const orderA = symptomOrder.indexOf(a.symptomKey);
                    const orderB = symptomOrder.indexOf(b.symptomKey);

                    // If symptom not in order list, put it at the end
                    if (orderA === -1 && orderB === -1) return 0;
                    if (orderA === -1) return 1;
                    if (orderB === -1) return -1;

                    return orderA - orderB;
                });

            // If no symptom data in the last 2 weeks, show default symptoms with 0 counts
            if (symptomTrends.length === 0) {
                const defaultSymptoms = ['cramps', 'bloating', 'diarrhea', 'constipation', 'fullness', 'mucus'];
                symptomTrends = defaultSymptoms.map(symptom => ({
                    symptom: getSymptomLabel(symptom),
                    trend: 'stable',
                    thisWeekCount: 0,
                    lastWeekCount: 0,
                    change: 0,
                }));
            }

            setHealthData({
                foodsToWatch: foodsToWatch,
                symptomTrends: symptomTrends,
            });

            // Fetch recommendations after successfully getting health data
            fetchRecommendations();
        } catch (error) {
            console.error('Error fetching health report:', error);
            setHealthData({
                foodsToWatch: [],
                symptomTrends: [],
            });
        } finally {
            setIsLoading(false);
        }
    };

    const fetchRecommendations = async () => {
        setIsLoadingRecommendations(true);
        try {
            const userId = localStorage.getItem('tummyai_user_id') || 'default_user';
            console.log('Fetching recommendations for user:', userId);
            const response = await apiClient.get(`/chat-assistant/${userId}`);
            console.log('Recommendations response:', response.data);
            setRecommendations(response.data.recommendations);
        } catch (error) {
            console.error('Error fetching recommendations:', error);
            console.error('Error details:', error.response?.data || error.message);
            setRecommendations(null);
        } finally {
            setIsLoadingRecommendations(false);
        }
    };

    const getRiskLevelColor = (level) => {
        switch (level) {
            case 'high':
                return 'text-destructive bg-destructive/10';
            case 'medium':
                return 'text-orange-600 bg-orange-100 dark:bg-orange-900/20';
            case 'low':
                return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20';
            default:
                return 'text-muted-foreground bg-muted';
        }
    };

    const getTrendIcon = (trend) => {
        switch (trend) {
            case 'increasing':
                return <TrendingUp className="h-5 w-5 text-red-600" />;
            case 'decreasing':
                return <TrendingDown className="h-5 w-5 text-green-600" />;
            case 'stable':
                return <Minus className="h-5 w-5 text-black dark:text-white" />;
            default:
                return null;
        }
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

    return (
        <div className="min-h-screen bg-background">
            <section className="py-16 px-4 sm:px-6 lg:px-8">
                <div className="max-w-7xl mx-auto">
                    <div className="mb-12">
                        <h1 className="text-4xl sm:text-5xl font-bold mb-4">Health Report</h1>
                        <p className="text-lg text-muted-foreground">
                            Personalized insights based on your meal history and symptoms
                        </p>
                    </div>

                    {isLoading ? (
                        <div className="text-center py-12">
                            <p className="text-muted-foreground">Loading health report...</p>
                        </div>
                    ) : !healthData ? (
                        <div className="text-center py-12">
                            <p className="text-muted-foreground">
                                No health data available. Start tracking your meals to see insights!
                            </p>
                        </div>
                    ) : (
                        <div className="space-y-12">
                            {/* Foods to Watch Section */}
                            <div>
                                <h2 className="text-3xl sm:text-4xl font-bold mb-6">
                                    Foods to Watch
                                </h2>
                                <p className="text-muted-foreground mb-6">
                                    These foods have been associated with your reported symptoms
                                </p>
                                {healthData.foodsToWatch && healthData.foodsToWatch.length > 0 ? (
                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                        {healthData.foodsToWatch.map((food, index) => (
                                            <Card key={index} className="p-6">
                                                <div className="flex items-start justify-between mb-4">
                                                    <div>
                                                        <h3 className="text-xl font-semibold mb-2">
                                                            {food.name}
                                                        </h3>
                                                    </div>
                                                    <span
                                                        className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getRiskLevelColor(
                                                            food.riskLevel
                                                        )}`}
                                                    >
                                                        {food.riskLevel} risk
                                                    </span>
                                                </div>
                                                <div className="space-y-3">
                                                    <div className="flex flex-wrap gap-2">
                                                        {food.symptomsTriggered.map(
                                                            (symptom, idx) => (
                                                                <span
                                                                    key={idx}
                                                                    className="px-2 py-1 bg-destructive/10 text-destructive rounded text-xs"
                                                                >
                                                                    {getSymptomLabel(symptom)}
                                                                </span>
                                                            )
                                                        )}
                                                    </div>
                                                </div>
                                            </Card>
                                        ))}
                                    </div>
                                ) : (
                                    <Card className="p-8 text-center">
                                        <p className="text-muted-foreground">
                                            Not enough data yet. Keep tracking your meals to identify patterns!
                                        </p>
                                    </Card>
                                )}
                            </div>

                            {/* Symptom Trends Section */}
                            <div>
                                <h2 className="text-3xl sm:text-4xl font-bold mb-6">
                                    Symptom Trends
                                </h2>
                                <p className="text-muted-foreground mb-6">
                                    Track how your symptoms are changing over time
                                </p>
                                {healthData.symptomTrends && healthData.symptomTrends.length > 0 ? (
                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                        {healthData.symptomTrends.map((item, index) => (
                                            <Card key={index} className="p-6">
                                                <div className="space-y-4">
                                                    <div>
                                                        <h3 className="text-lg font-semibold">
                                                            {item.symptom}
                                                        </h3>
                                                    </div>
                                                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                                                        {getTrendIcon(item.trend)}
                                                        <span>
                                                            this week: {item.thisWeekCount}
                                                        </span>
                                                        <span>
                                                            last week: {item.lastWeekCount}
                                                        </span>
                                                    </div>
                                                </div>
                                            </Card>
                                        ))}
                                    </div>
                                ) : (
                                    <Card className="p-8 text-center">
                                        <p className="text-muted-foreground">
                                            Not enough data yet. Keep tracking your meals to see trends!
                                        </p>
                                    </Card>
                                )}
                            </div>

                            {/* Recommendations Section */}
                            <Card className="p-8 bg-primary/5 border-primary/20">
                                <h2 className="text-2xl font-bold mb-4">Recommendations</h2>
                                {isLoadingRecommendations ? (
                                    <p className="text-muted-foreground">Loading personalized recommendations...</p>
                                ) : recommendations ? (
                                    <div className="text-muted-foreground">
                                        <div className="whitespace-pre-wrap leading-loose">{recommendations}</div>
                                    </div>
                                ) : (
                                    <ul className="space-y-3 text-muted-foreground">
                                        <li className="flex items-start gap-2">
                                            <span className="text-primary font-bold">•</span>
                                            <span>
                                                Consider reducing or eliminating high-risk foods from
                                                your diet
                                            </span>
                                        </li>
                                        <li className="flex items-start gap-2">
                                            <span className="text-primary font-bold">•</span>
                                            <span>
                                                Keep tracking your meals to identify more patterns
                                            </span>
                                        </li>
                                        <li className="flex items-start gap-2">
                                            <span className="text-primary font-bold">•</span>
                                            <span>
                                                Consult with a healthcare professional for personalized
                                                advice
                                            </span>
                                        </li>
                                        <li className="flex items-start gap-2">
                                            <span className="text-primary font-bold">•</span>
                                            <span>
                                                Monitor how symptoms change when adjusting your diet
                                            </span>
                                        </li>
                                    </ul>
                                )}
                            </Card>
                        </div>
                    )}
                </div>
            </section>
        </div>
    );
}
