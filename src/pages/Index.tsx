import React from 'react';
const Index = () => {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center max-w-3xl p-8 bg-white rounded-lg shadow-lg">
          <h1 className="text-4xl font-bold mb-4">Review Authenticity Analyzer</h1>
          <p className="text-xl text-gray-600 mb-6">
            This application is implemented using Python and Streamlit rather than React/TypeScript.
          </p>
          <div className="bg-blue-50 p-6 rounded-lg border border-blue-200 text-left">
            <h2 className="text-2xl font-semibold mb-4 text-blue-800">How to Run This Application</h2>
            <ol className="list-decimal list-inside space-y-3 text-gray-700">
              <li>Clone this repository to your local machine</li>
              <li>Navigate to the root directory of the project</li>
              <li>Install the required Python packages by running:<br/>
                <code className="bg-gray-200 px-2 py-1 rounded">pip install -r requirements.txt</code>
              </li>
              <li>Run the Streamlit application with:<br/>
                <code className="bg-gray-200 px-2 py-1 rounded">streamlit run src/app.py</code>
              </li>
            </ol>
            <div className="mt-6 bg-yellow-50 p-4 rounded-lg border border-yellow-200">
              <h3 className="font-semibold text-yellow-800">Features</h3>
              <ul className="list-disc list-inside text-gray-700 mt-2">
                <li>URL input for product pages</li>
                <li>Review scraping from e-commerce websites</li>
                <li>NLP-based fake review detection</li>
                <li>Analysis results with percentage of real vs fake reviews</li>
                <li>Visualization of review authenticity</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  };
  
  export default Index;
  