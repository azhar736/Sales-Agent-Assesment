interface CompanyAnalysisProps {
  analysis: {
    companyAnalysis: {
      challenges: string[];
      opportunities: string[];
      marketPosition: string;
    };
  };
}

export function CompanyAnalysis({ analysis }: CompanyAnalysisProps) {
  const { companyAnalysis } = analysis;

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Company Analysis</h2>
      
      <div className="space-y-4">
        <div>
          <h3 className="font-medium text-gray-700 mb-2">Market Position</h3>
          <p className="text-gray-600">{companyAnalysis.marketPosition}</p>
        </div>

        <div>
          <h3 className="font-medium text-gray-700 mb-2">Key Challenges</h3>
          <ul className="list-disc list-inside text-gray-600">
            {companyAnalysis.challenges.map((challenge, index) => (
              <li key={index}>{challenge}</li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="font-medium text-gray-700 mb-2">Opportunities</h3>
          <ul className="list-disc list-inside text-gray-600">
            {companyAnalysis.opportunities.map((opportunity, index) => (
              <li key={index}>{opportunity}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
} 