import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Sparkles, Globe, X as CloseIcon } from 'lucide-react';

export const LandingFooter = () => {
  const navigate = useNavigate();
  const [modalContent, setModalContent] = useState(null);

  const handleLinkClick = (e, target) => {
    e.preventDefault();
    if (typeof target === 'string' && target.startsWith('/')) {
      navigate(target);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (typeof target === 'object') {
      setModalContent(target);
    }
  };

  const infoPages = {
    about: {
      title: "About Veyra",
      content: "Veyra is an advanced AI-powered career intelligence and personalized learning path platform. Designed to bridge the gap between educational foundations and high-impact tech careers, Veyra builds dynamic roadmaps, provides hands-on project verification, and delivers real-time skill assessments tailored to every learner."
    },
    careers: {
      title: "Careers at Veyra",
      content: "Join our mission to democratize technical education and career growth. We are actively hiring AI Engineers, Full-Stack Developers, Content Engineers, and Technical Curriculum Specialists. Contact careers@veyra.ai to explore open roles."
    },
    privacy: {
      title: "Privacy Policy",
      content: "Veyra values your privacy. We store user profile details, learning progress, and repository submissions strictly to customize your personalized learning path. We do not sell your personal data to third parties. All authentication credentials and API keys are stored with industry-standard encryption."
    },
    terms: {
      title: "Terms of Service",
      content: "By using Veyra, you agree to submit original work for project evaluations and assessments. Automated evaluations are intended for personal learning and career preparation. Commercial redistribution of Veyra curriculum content without written consent is strictly prohibited."
    },
    security: {
      title: "Security & Compliance",
      content: "Veyra maintains strict security standards including JWT-based session security, HTTPS encryption in transit, isolated code execution environments, and zero trust storage for user repositories."
    },
    documentation: {
      title: "Platform Documentation",
      content: "Welcome to Veyra Documentation. Explore our Path Engine algorithms, GitHub project evaluation pipelines, Google Colab verification rules, and progress tracking architecture."
    },
    community: {
      title: "Developer Community",
      content: "Connect with fellow learners, review peer projects, share interview prep experiences, and get assistance from AI mentors in the Veyra community ecosystem."
    }
  };

  return (
    <>
      <footer className="bg-[#0F172A] text-slate-400 border-t border-slate-800 pt-16 pb-12 px-6 lg:px-12">
        <div className="max-w-7xl mx-auto space-y-12">
          {/* Top Branding & Socials */}
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-10 border-b border-slate-800">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <img
                  src="/veyra-logo.png"
                  alt="Veyra Logo"
                  className="w-7 h-7 rounded-lg object-contain shadow-sm border border-white/20 shrink-0"
                />
                <span className="text-xl font-extrabold text-white tracking-tight">Veyra</span>
              </div>
              <p className="text-sm text-slate-400 max-w-md">
                AI-powered career intelligence and personalized learning path construction.
              </p>
            </div>

            {/* Required Social Icons */}
            <div className="flex items-center gap-3">
              {/* GitHub Icon */}
              <a
                href="https://github.com/2k24aids065-sketch"
                target="_blank"
                rel="noopener noreferrer"
                className="w-9 h-9 rounded-full bg-[#181E25] flex items-center justify-center text-white hover:bg-white hover:text-[#0A0A0A] transition-colors"
                aria-label="GitHub Profile"
                title="GitHub Profile"
              >
                <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                  <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
                </svg>
              </a>

              {/* X (Twitter) Icon */}
              <a
                href="https://x.com/Veyra_Path"
                target="_blank"
                rel="noopener noreferrer"
                className="w-9 h-9 rounded-full bg-[#181E25] flex items-center justify-center text-white hover:bg-white hover:text-[#0A0A0A] transition-colors"
                aria-label="X Profile"
                title="X Profile"
              >
                <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                </svg>
              </a>

              {/* PathPilot Website Home Icon */}
              <button
                onClick={(e) => {
                  e.preventDefault();
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                  navigate('/');
                }}
                className="w-9 h-9 rounded-full bg-[#181E25] flex items-center justify-center text-white hover:bg-white hover:text-[#0A0A0A] transition-colors"
                aria-label="PathPilot Website"
                title="PathPilot Home"
              >
                <Globe className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* 5 Column Sections: Product, Learning, Projects, Resources, Company */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-8 text-sm">
            <div>
              <h4 className="font-semibold text-white mb-4">Product</h4>
              <ul className="space-y-2.5">
                <li><a href="/career-analysis" onClick={(e) => handleLinkClick(e, '/career-analysis')} className="hover:text-white transition-colors">Career Intelligence</a></li>
                <li><a href="/learning-path" onClick={(e) => handleLinkClick(e, '/learning-path')} className="hover:text-white transition-colors">Path Engine</a></li>
                <li><a href="/profile" onClick={(e) => handleLinkClick(e, '/profile')} className="hover:text-white transition-colors">Profile Analysis</a></li>
                <li><a href="/skill-gap" onClick={(e) => handleLinkClick(e, '/skill-gap')} className="hover:text-white transition-colors">Skill Matrix</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Learning</h4>
              <ul className="space-y-2.5">
                <li><a href="/courses" onClick={(e) => handleLinkClick(e, '/courses')} className="hover:text-white transition-colors">Frontend Path</a></li>
                <li><a href="/courses" onClick={(e) => handleLinkClick(e, '/courses')} className="hover:text-white transition-colors">Backend Path</a></li>
                <li><a href="/courses" onClick={(e) => handleLinkClick(e, '/courses')} className="hover:text-white transition-colors">Cybersecurity Path</a></li>
                <li><a href="/courses" onClick={(e) => handleLinkClick(e, '/courses')} className="hover:text-white transition-colors">SDE Path</a></li>
                <li><a href="/courses" onClick={(e) => handleLinkClick(e, '/courses')} className="hover:text-white transition-colors">AI Engineer Path</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Projects</h4>
              <ul className="space-y-2.5">
                <li><a href="/projects" onClick={(e) => handleLinkClick(e, '/projects')} className="hover:text-white transition-colors">Project Catalog</a></li>
                <li><a href="/projects" onClick={(e) => handleLinkClick(e, '/projects')} className="hover:text-white transition-colors">GitHub Review Engine</a></li>
                <li><a href="/projects" onClick={(e) => handleLinkClick(e, '/projects')} className="hover:text-white transition-colors">Colab Verification</a></li>
                <li><a href="/assessments" onClick={(e) => handleLinkClick(e, '/assessments')} className="hover:text-white transition-colors">Project Assessments</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Resources</h4>
              <ul className="space-y-2.5">
                <li><a href="#" onClick={(e) => handleLinkClick(e, infoPages.documentation)} className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="/learning-path" onClick={(e) => handleLinkClick(e, '/learning-path')} className="hover:text-white transition-colors">Career Roadmaps</a></li>
                <li><a href="/skill-gap" onClick={(e) => handleLinkClick(e, '/skill-gap')} className="hover:text-white transition-colors">Skill Benchmarks</a></li>
                <li><a href="#" onClick={(e) => handleLinkClick(e, infoPages.community)} className="hover:text-white transition-colors">Community</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Company</h4>
              <ul className="space-y-2.5">
                <li><a href="#" onClick={(e) => handleLinkClick(e, infoPages.about)} className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" onClick={(e) => handleLinkClick(e, infoPages.careers)} className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" onClick={(e) => handleLinkClick(e, infoPages.privacy)} className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" onClick={(e) => handleLinkClick(e, infoPages.terms)} className="hover:text-white transition-colors">Terms of Service</a></li>
              </ul>
            </div>
          </div>

          {/* Bottom Copyright Strip */}
          <div className="pt-8 border-t border-[#222222] flex flex-col sm:flex-row items-center justify-between text-xs text-[#8E8E93] gap-4">
            <span>&copy; 2026 Veyra Inc. All rights reserved.</span>
            <div className="flex gap-6">
              <a href="#" onClick={(e) => handleLinkClick(e, infoPages.privacy)} className="hover:text-white transition-colors">Privacy</a>
              <a href="#" onClick={(e) => handleLinkClick(e, infoPages.terms)} className="hover:text-white transition-colors">Terms</a>
              <a href="#" onClick={(e) => handleLinkClick(e, infoPages.security)} className="hover:text-white transition-colors">Security</a>
            </div>
          </div>
        </div>
      </footer>

      {/* Info Modal for Company/Resource Links */}
      {modalContent && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fadeIn">
          <div className="bg-[#121212] border border-[#2A2A2A] rounded-2xl p-6 sm:p-8 max-w-lg w-full text-white space-y-4 relative shadow-2xl">
            <button
              onClick={() => setModalContent(null)}
              className="absolute top-4 right-4 p-1.5 rounded-full bg-[#1F1F1F] text-[#8E8E93] hover:text-white hover:bg-[#2A2A2A] transition-colors"
              aria-label="Close"
            >
              <CloseIcon className="w-4 h-4" />
            </button>

            <div className="flex items-center gap-2">
              <img
                src="/veyra-logo.png"
                alt="Veyra Logo"
                className="w-6 h-6 rounded-md object-contain shadow-sm shrink-0"
              />
              <h3 className="text-lg font-bold text-white tracking-tight">{modalContent.title}</h3>
            </div>

            <p className="text-sm text-[#A0A0A0] leading-relaxed">
              {modalContent.content}
            </p>

            <div className="pt-4 flex justify-end">
              <button
                onClick={() => setModalContent(null)}
                className="px-5 py-2 rounded-full bg-white text-[#0A0A0A] font-bold text-xs hover:bg-gray-200 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
