export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
}

export interface CompanyData {
  id: string;
  name: string;
  industry: string;
  size: string;
}

export interface SalesAnalysis {
  productId: string;
  companyId: string;
  recommendation: string;
  score: number;
} 