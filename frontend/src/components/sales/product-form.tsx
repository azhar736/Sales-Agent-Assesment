'use client';

import { useState } from 'react';
import { Input } from '../ui/form/input';
import { TextArea } from '../ui/form/text-area';

interface ProductFormProps {
  onSubmit: (data: FormData) => Promise<void>;
  isLoading: boolean;
}

export function ProductForm({ onSubmit, isLoading }: ProductFormProps) {
  const [formData, setFormData] = useState({
    productName: '',
    productDescription: '',
    price: '',
    companyUrl: '',
    competitors: '',
    additionalNotes: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    await onSubmit(formData);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      // Simulate upload progress
      setUploadProgress(0);
      const interval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            return 100;
          }
          return prev + 10;
        });
      }, 100);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Input
        label="Product Name"
        name="productName"
        value={formData.productName}
        onChange={handleChange}
        error={errors.productName}
        disabled={isLoading}
      />

      <TextArea
        label="Product Description"
        name="productDescription"
        value={formData.productDescription}
        onChange={handleChange}
        error={errors.productDescription}
        rows={4}
        disabled={isLoading}
      />

      <Input
        label="Price"
        name="price"
        type="number"
        value={formData.price}
        onChange={handleChange}
        error={errors.price}
        disabled={isLoading}
      />

      <Input
        label="Company URL"
        name="companyUrl"
        type="url"
        value={formData.companyUrl}
        onChange={handleChange}
        error={errors.companyUrl}
        disabled={isLoading}
      />

      <TextArea
        label="Competitors (one per line)"
        name="competitors"
        value={formData.competitors}
        onChange={handleChange}
        rows={3}
        disabled={isLoading}
      />

      <div>
        <label htmlFor="file" className="block text-sm font-medium text-gray-700">
          Additional Documents
        </label>
        <input
          type="file"
          id="file"
          name="file"
          onChange={handleFileChange}
          disabled={isLoading}
          className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50"
        />
        {selectedFile && (
          <div className="mt-2">
            <div className="text-sm text-gray-600">{selectedFile.name}</div>
            <div className="mt-1 h-2 w-full bg-gray-200 rounded-full">
              <div
                className="h-2 bg-blue-600 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          </div>
        )}
      </div>

      <TextArea
        label="Additional Notes"
        name="additionalNotes"
        value={formData.additionalNotes}
        onChange={handleChange}
        rows={3}
        disabled={isLoading}
      />

      <button
        type="submit"
        disabled={isLoading}
        className={`w-full py-2 px-4 rounded-md text-white font-medium
          ${isLoading 
            ? 'bg-blue-400 cursor-not-allowed' 
            : 'bg-blue-500 hover:bg-blue-600'
          }`}
      >
        {isLoading ? (
          <>
            <svg
              className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            Analyzing...
          </>
        ) : (
          'Analyze'
        )}
      </button>
    </form>
  );
} 