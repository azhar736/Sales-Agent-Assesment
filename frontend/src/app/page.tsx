'use client';

import { useState } from 'react';
import { ProductForm } from '@/components/sales/product-form';
import { CompanyAnalysis } from '@/components/sales/company-analysis';
import { ResultsDisplay } from '@/components/sales/results-display';

interface AnalysisResult {
  companyAnalysis: {
    challenges: string[];
    opportunities: string[];
    marketPosition: string;
  };
  salesStrategy: {
    valueProposition: string;
    keyPoints: string[];
    recommendations: string[];
  };
}

export default function Home() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleAnalysis = async (formData: FormData) => {
    setIsAnalyzing(true);
    setError(null);
    setSuccess(false);
    
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to analyze data');
      }

      const result = await response.json();
      setAnalysisResult(result);
      setSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setAnalysisResult(null);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-8">AI Sales Assistant</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <ProductForm onSubmit={handleAnalysis} isLoading={isAnalyzing} />
          
          {error && (
            <div className="mt-4 p-4 bg-red-50 text-red-600 rounded-md">
              {error}
            </div>
          )}
          
          {success && (
            <div className="mt-4 p-4 bg-green-50 text-green-600 rounded-md">
              Analysis completed successfully!
            </div>
          )}
        </div>
        
        <div>
          {isAnalyzing ? (
            <div className="flex items-center justify-center h-full">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
            </div>
          ) : analysisResult ? (
            <div className="space-y-6">
              <CompanyAnalysis analysis={analysisResult} />
              <ResultsDisplay results={analysisResult} />
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
