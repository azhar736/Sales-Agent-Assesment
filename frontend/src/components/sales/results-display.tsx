interface ResultsDisplayProps {
  results: {
    salesStrategy?: {
      valueProposition: string;
      keyPoints: string[];
      recommendations: string[];
    };
  };
}

export function ResultsDisplay({ results }: ResultsDisplayProps) {
  const { salesStrategy } = results;
  
  if (!salesStrategy) return null;

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Sales Strategy</h2>
      <div className="space-y-4">
        <div>
          <h3 className="font-medium text-gray-700 mb-2">Value Proposition</h3>
          <p className="text-gray-600">{salesStrategy.valueProposition}</p>
        </div>
        <div>
          <h3 className="font-medium text-gray-700 mb-2">Key Points</h3>
          <ul className="list-disc list-inside text-gray-600">
            {salesStrategy.keyPoints.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
} 