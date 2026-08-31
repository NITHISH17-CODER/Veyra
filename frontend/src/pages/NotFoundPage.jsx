import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/common/Button';
import { Compass, Home } from 'lucide-react';

export const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center p-6 text-center">
      <div className="max-w-md bg-white rounded-3xl border border-[#E5E7EB] p-8 space-y-6">
        <div className="w-16 h-16 rounded-full bg-[#F7F8FA] text-[#0A0A0A] mx-auto flex items-center justify-center">
          <Compass className="w-8 h-8 animate-spin" />
        </div>
        <div className="space-y-2">
          <h1 className="text-3xl font-bold text-[#0A0A0A]">404 — Page Not Found</h1>
          <p className="text-xs text-[#8E8E93]">The route you requested could not be mapped.</p>
        </div>
        <Button
          variant="primary"
          size="md"
          icon={Home}
          onClick={() => navigate('/dashboard')}
          className="w-full"
        >
          Return to Dashboard
        </Button>
      </div>
    </div>
  );
};
