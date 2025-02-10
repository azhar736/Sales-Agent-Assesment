import { fetchJson } from './api';

export interface AnalysisRequest {
  productName: string;
  productDescription: string;
  price: string;
  companyUrl: string;
  competitors?: string;
  additionalNotes?: string;
  file?: File;
}

export interface AnalysisResponse {
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

export async function analyzeSalesOpportunity(
  data: AnalysisRequest
): Promise<AnalysisResponse> {
  const formData = new FormData();
  
  // Add all text fields
  Object.entries(data).forEach(([key, value]) => {
    if (key !== 'file' && value) {
      formData.append(key, value);
    }
  });

  // Add file if present
  if (data.file) {
    formData.append('file', data.file);
  }

  return fetchJson<AnalysisResponse>('/api/analyze', {
    method: 'POST',
    body: formData,
  });
} 