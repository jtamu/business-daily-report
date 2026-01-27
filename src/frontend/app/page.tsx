export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          営業日報システム
        </h1>
        <p className="text-gray-600 mb-8">
          営業担当者が日々の顧客訪問活動を記録し、上長がフィードバックを提供するシステム
        </p>
        <div className="space-x-4">
          <a
            href="/login"
            className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            ログイン
          </a>
        </div>
      </div>
    </main>
  );
}
