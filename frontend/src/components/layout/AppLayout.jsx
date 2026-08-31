import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';
import { MobileNav } from './MobileNav';
import { Toast } from '../common/Toast';
import { WhyModal } from '../common/WhyModal';
import { FeedbackModal } from '../common/FeedbackModal';
import { FloatingChatbot } from '../common/FloatingChatbot';

export const AppLayout = () => {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#F4F5FA] text-slate-900 flex flex-col pb-16 lg:pb-0 font-sans antialiased">
      {/* Collapsible Sidebar */}
      <Sidebar mobileOpen={mobileSidebarOpen} setMobileOpen={setMobileSidebarOpen} />

      {/* Main Content Container with fixed padding for collapsed sidebar */}
      <div className="lg:pl-20 flex-1 flex flex-col min-h-screen transition-all duration-300">
        <Topbar onOpenMobileMenu={() => setMobileSidebarOpen(true)} />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto space-y-8">
          <Outlet />
        </main>
      </div>

      {/* Mobile Bottom Navigation */}
      <MobileNav />

      {/* Modals & Toast overlay */}
      <Toast />
      <WhyModal />
      <FeedbackModal />

      {/* Floating AI Chatbot Widget */}
      <FloatingChatbot />
    </div>
  );
};
