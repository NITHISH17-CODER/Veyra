import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import { Sparkles, ArrowRight, Menu, X } from 'lucide-react';
import { Button } from '../common/Button';

export const LandingNavbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeSection, setActiveSection] = useState('');
  const [isScrolled, setIsScrolled] = useState(false);

  const navLinks = [
    { name: 'Features', href: '#features', id: 'features' },
    { name: 'How It Works', href: '#how-it-works', id: 'how-it-works' },
    { name: 'Learning Paths', href: '#learning-paths', id: 'learning-paths' },
    { name: 'AI Analysis', href: '#ai-analysis', id: 'ai-analysis' },
  ];

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);

      if (location.pathname !== '/') return;

      const scrollPosition = window.scrollY + 100;
      for (const link of navLinks) {
        const element = document.getElementById(link.id);
        if (element) {
          const top = element.offsetTop;
          const height = element.offsetHeight;
          if (scrollPosition >= top && scrollPosition < top + height) {
            setActiveSection(link.id);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [location.pathname]);

  const handleNavClick = (e, href, id) => {
    e.preventDefault();
    setMobileMenuOpen(false);
    if (location.pathname !== '/') {
      navigate('/' + href);
      return;
    }
    const element = document.getElementById(id);
    if (element) {
      const navOffset = 70;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - navOffset;
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  };

  return (
    <header className={`w-full fixed top-0 z-50 h-[72px] flex items-center px-6 lg:px-12 transition-all duration-300 ${
      isScrolled
        ? 'bg-white/85 backdrop-blur-xl border-b border-slate-200/50 shadow-sm'
        : 'bg-transparent border-b border-transparent'
    }`}>
      <div className="max-w-7xl w-full mx-auto flex items-center justify-between">
        {/* Left: Veyra Brand Logo */}
        <NavLink to="/" className="flex items-center gap-2.5 group">
          <img
            src="/veyra-logo.png"
            alt="Veyra Logo"
            className="w-8 h-8 rounded-xl object-contain shadow-sm border border-[#146EF5]/20 shrink-0 group-hover:scale-105 transition-transform"
          />
          <span className="text-xl font-extrabold text-[#111827] tracking-tight font-sans">Veyra</span>
        </NavLink>

        {/* Center Navigation Links - White / Light Blue Nav Buttons */}
        <nav className="hidden md:flex items-center gap-2.5">
          {navLinks.map((link) => {
            const isActive = activeSection === link.id;
            return (
              <a
                key={link.id}
                href={link.href}
                onClick={(e) => handleNavClick(e, link.href, link.id)}
                className={`text-xs font-bold px-4 py-2 rounded-full transition-all duration-200 cursor-pointer border ${
                  isActive
                    ? 'bg-[#146EF5] text-white border-[#146EF5] shadow-sm shadow-blue-500/20'
                    : 'bg-white text-[#111827] border-[#DCE6F2] hover:bg-[#EAF3FF] hover:text-[#146EF5] hover:border-[#146EF5]'
                }`}
              >
                {link.name}
              </a>
            );
          })}
        </nav>

        {/* Right: Actions */}
        <div className="hidden md:flex items-center gap-3">
          <NavLink
            to="/login"
            className="text-xs font-bold text-[#111827] hover:text-[#146EF5] transition-colors px-3 py-2"
          >
            Log In
          </NavLink>

          <Button
            variant="outline"
            size="md"
            icon={ArrowRight}
            iconPosition="right"
            onClick={() => navigate('/register')}
            className="bg-white text-[#111827] border border-[#DCE6F2] shadow-xs hover:bg-[#EAF3FF] hover:text-[#146EF5] hover:border-[#146EF5] rounded-full px-5 py-2 text-xs font-bold transition-all duration-200"
          >
            Get Started
          </Button>
        </div>

        {/* Mobile Hamburger Button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 rounded-2xl text-[#111827] hover:bg-[#EAF3FF] backdrop-blur-md transition-colors"
          aria-label="Toggle navigation"
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="absolute top-[72px] left-0 w-full bg-white/95 backdrop-blur-2xl border-b border-[#DCE6F2] p-6 shadow-2xl md:hidden space-y-3 animate-fadeIn">
          {navLinks.map((link) => (
            <a
              key={link.id}
              href={link.href}
              onClick={(e) => handleNavClick(e, link.href, link.id)}
              className="block text-sm font-bold text-[#111827] bg-[#F5F9FF] border border-[#DCE6F2] px-4 py-2.5 rounded-full text-center hover:bg-[#146EF5] hover:text-white hover:border-[#146EF5] transition-colors"
            >
              {link.name}
            </a>
          ))}
          <div className="pt-4 border-t border-[#DCE6F2] flex flex-col gap-3">
            <NavLink
              to="/login"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full text-center py-2.5 rounded-full border border-[#DCE6F2] text-[#111827] text-sm font-bold bg-white hover:bg-[#EAF3FF] hover:text-[#146EF5]"
            >
              Log In
            </NavLink>
            <Button
              variant="primary"
              size="md"
              onClick={() => {
                setMobileMenuOpen(false);
                navigate('/register');
              }}
              className="w-full justify-center rounded-full py-2.5"
            >
              Get Started
            </Button>
          </div>
        </div>
      )}
    </header>
  );
};
