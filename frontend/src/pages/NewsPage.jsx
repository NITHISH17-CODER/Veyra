import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Card } from '../components/common/Card';
import { Badge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { LoadingState } from '../components/common/LoadingState';
import {
  Newspaper, ExternalLink, Sparkles, Clock, X, ArrowRight, AlertCircle, RefreshCw, Zap, Globe, Tag
} from 'lucide-react';

export const NewsPage = () => {
  const { id: routeArticleId } = useParams();
  const navigate = useNavigate();

  const [newsData, setNewsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('For You');
  const [selectedArticle, setSelectedArticle] = useState(null);

  const fetchNews = async () => {
    setLoading(true);
    setError(null);
    try {
      const param = selectedCategory === 'For You' ? 'All' : selectedCategory;
      const res = await api.get(`/news?category=${encodeURIComponent(param)}`);
      setNewsData(res.data);
    } catch (err) {
      console.error("Failed fetching news:", err);
      setError("Failed to load technical news. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNews();
  }, [selectedCategory]);

  // Handle route parameter /news/:id
  useEffect(() => {
    if (routeArticleId) {
      const fetchArticleDetail = async () => {
        try {
          const res = await api.get(`/news/${routeArticleId}`);
          if (res.data && res.data.article) {
            setSelectedArticle(res.data.article);
          }
        } catch (e) {
          console.warn("Failed fetching article detail:", e);
        }
      };
      fetchArticleDetail();
    } else {
      setSelectedArticle(null);
    }
  }, [routeArticleId]);

  const categories = ['For You', 'AI', 'Frontend', 'Backend', 'Cybersecurity', 'SDE'];
  const allArticles = newsData?.articles || [];
  const personalizedArticles = newsData?.personalized_articles || [];
  const otherArticles = newsData?.other_articles || [];

  // Ticker headlines
  const tickerHeadlines = allArticles.slice(0, 12).map(a => a.title);

  const handleOpenArticle = (article) => {
    setSelectedArticle(article);
    if (article.id) {
      navigate(`/news/${article.id}`, { replace: false });
    }
  };

  const handleCloseArticle = () => {
    setSelectedArticle(null);
    if (routeArticleId) {
      navigate('/news', { replace: false });
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">LATEST TECHNICAL NEWS</span>
          {newsData?.user_course && (
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-[#1456F0] text-white flex items-center gap-1">
              <Sparkles className="w-3 h-3" /> Personalized for {newsData.user_course}
            </span>
          )}
        </div>
        <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">Technical Pulse & Industry News</h1>
        <p className="text-sm text-[#45515E]">
          Stay informed with curated technical updates tailored to your career path.
        </p>
      </div>

      {/* MOVING HEADLINE TICKER — VEYRA BLUE VISUAL IDENTITY */}
      {tickerHeadlines.length > 0 && (
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#1456F0] via-[#0B5ED7] to-[#1456F0] border border-[#1456F0] shadow-md">
          <div className="flex items-center">
            <div className="shrink-0 px-4 py-3 bg-white/20 backdrop-blur-md text-white text-[10px] font-extrabold uppercase tracking-widest flex items-center gap-1.5 z-10 border-r border-white/20">
              <Zap className="w-3.5 h-3.5 text-yellow-300 fill-yellow-300" />
              LATEST TECH
            </div>
            <div className="overflow-hidden flex-1 py-3">
              <div
                className="flex items-center gap-6 animate-ticker whitespace-nowrap"
                style={{
                  animation: `ticker ${Math.max(tickerHeadlines.length * 4, 20)}s linear infinite`,
                }}
              >
                {[...tickerHeadlines, ...tickerHeadlines].map((headline, idx) => (
                  <span key={idx} className="text-xs font-semibold text-white flex items-center gap-2 shrink-0">
                    <span className="text-blue-200 font-bold">→</span>
                    {headline}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Ticker CSS animation */}
      <style>{`
        @keyframes ticker {
          0% { transform: translateX(0%); }
          100% { transform: translateX(-50%); }
        }
        .animate-ticker {
          will-change: transform;
        }
      `}</style>

      {/* CATEGORY FILTER TABS */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-4 py-1.5 text-xs font-semibold rounded-full transition-all whitespace-nowrap ${
              selectedCategory === cat
                ? 'bg-[#0A0A0A] text-white'
                : 'bg-[#F7F8FA] text-[#45515E] hover:bg-[#F2F3F5] border border-[#E5E7EB]'
            }`}
          >
            {cat === 'For You' ? '✨ For You' : cat}
          </button>
        ))}
      </div>

      {/* CONTENT */}
      {loading ? (
        <LoadingState message="Loading latest technical news..." />
      ) : error ? (
        <Card radius="20" className="p-8 text-center space-y-4">
          <AlertCircle className="w-12 h-12 text-red-400 mx-auto" />
          <h3 className="text-lg font-bold text-[#0A0A0A]">{error}</h3>
          <Button variant="outline" size="sm" icon={RefreshCw} onClick={fetchNews}>
            Retry
          </Button>
        </Card>
      ) : allArticles.length === 0 ? (
        <Card radius="20" className="p-8 text-center space-y-4">
          <Newspaper className="w-12 h-12 text-[#8E8E93] mx-auto" />
          <h3 className="text-lg font-bold text-[#0A0A0A]">No news articles available</h3>
          <p className="text-sm text-[#45515E]">Try selecting a different category or check back later.</p>
          <Button variant="outline" size="sm" icon={RefreshCw} onClick={fetchNews}>
            Refresh
          </Button>
        </Card>
      ) : (
        <div className="space-y-8">
          {/* PERSONALIZED ARTICLES SECTION */}
          {selectedCategory === 'For You' && personalizedArticles.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-lg font-bold text-[#0A0A0A] flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-orange-500" />
                <span>Recommended For Your Career Path</span>
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {personalizedArticles.map(article => (
                  <Card
                    key={article.id}
                    radius="20"
                    className="p-6 space-y-4 flex flex-col justify-between bg-white border border-[#E5E7EB] hover:border-[#0A0A0A] transition-all cursor-pointer group"
                    onClick={() => handleOpenArticle(article)}
                  >
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <Badge variant="dark">{article.category}</Badge>
                        <span className="text-[11px] text-[#8E8E93] flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {new Date(article.publishedAt || Date.now()).toLocaleDateString()}
                        </span>
                      </div>
                      <h3 className="text-lg font-bold text-[#0A0A0A] leading-snug group-hover:text-blue-700 transition-colors">{article.title}</h3>
                      <p className="text-xs text-[#45515E] leading-relaxed line-clamp-3">{article.description}</p>
                    </div>

                    <div className="pt-4 border-t border-[#E5E7EB] flex items-center justify-between text-xs">
                      <span className="font-semibold text-[#8E8E93] truncate max-w-[180px]">{article.source}</span>
                      <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#0A0A0A] text-white font-semibold text-xs group-hover:bg-[#222] transition-colors">
                        <span>Read Inside</span>
                        <ArrowRight className="w-3 h-3" />
                      </span>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {/* OTHER TECHNICAL NEWS SECTION */}
          <div className="space-y-4">
            <h2 className="text-lg font-bold text-[#0A0A0A] flex items-center gap-2">
              <Newspaper className="w-4 h-4 text-[#0A0A0A]" />
              <span>{selectedCategory === 'For You' ? 'Other Technical News' : `${selectedCategory} News`}</span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {(selectedCategory === 'For You' ? otherArticles : allArticles).map(article => (
                <Card
                  key={article.id}
                  radius="16"
                  className="p-6 space-y-4 flex flex-col justify-between bg-white border border-[#E5E7EB] hover:border-[#0A0A0A] transition-all cursor-pointer group"
                  onClick={() => handleOpenArticle(article)}
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Badge variant="surface">{article.category}</Badge>
                      <span className="text-[10px] text-[#8E8E93]">
                        {new Date(article.publishedAt || Date.now()).toLocaleDateString()}
                      </span>
                    </div>
                    <h3 className="text-base font-bold text-[#0A0A0A] leading-snug line-clamp-2 group-hover:text-blue-700 transition-colors">{article.title}</h3>
                    <p className="text-xs text-[#45515E] line-clamp-3 leading-relaxed">{article.description}</p>
                  </div>

                  <div className="pt-3 border-t border-[#E5E7EB] flex items-center justify-between text-xs">
                    <span className="font-medium text-[#8E8E93] truncate max-w-[140px]">{article.source}</span>
                    <span className="inline-flex items-center gap-1 text-xs font-bold text-[#0A0A0A] group-hover:text-blue-700">
                      <span>Read</span>
                      <ArrowRight className="w-3 h-3" />
                    </span>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* INTERNAL NEWS DETAIL MODAL */}
      {selectedArticle && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
          onClick={handleCloseArticle}
        >
          <div
            className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[85vh] overflow-y-auto animate-fadeIn"
            onClick={e => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="sticky top-0 bg-white z-10 px-8 pt-6 pb-4 border-b border-[#E5E7EB] flex items-start justify-between gap-4 rounded-t-3xl">
              <div className="space-y-2 min-w-0">
                <div className="flex items-center gap-2">
                  <Badge variant="dark">{selectedArticle.category}</Badge>
                  <span className="text-[10px] text-[#8E8E93] flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {new Date(selectedArticle.publishedAt || Date.now()).toLocaleDateString('en-US', {
                      year: 'numeric', month: 'long', day: 'numeric'
                    })}
                  </span>
                </div>
                <h2 className="text-xl font-bold text-[#0A0A0A] leading-snug">{selectedArticle.title}</h2>
              </div>
              <button
                onClick={handleCloseArticle}
                className="p-2 rounded-full hover:bg-[#F2F3F5] transition-colors shrink-0"
              >
                <X className="w-5 h-5 text-[#45515E]" />
              </button>
            </div>

            {/* Modal Content */}
            <div className="px-8 py-6 space-y-6">
              {/* Source Info */}
              <div className="flex items-center gap-3 p-4 rounded-2xl bg-[#F7F8FA] border border-[#E5E7EB]">
                <Globe className="w-5 h-5 text-[#8E8E93] shrink-0" />
                <div>
                  <span className="text-xs font-bold text-[#0A0A0A] block">{selectedArticle.source}</span>
                  <span className="text-[10px] text-[#8E8E93]">Original Source</span>
                </div>
              </div>

              {/* Tags */}
              {selectedArticle.tags && selectedArticle.tags.length > 0 && (
                <div className="flex items-center gap-2 flex-wrap">
                  <Tag className="w-3.5 h-3.5 text-[#8E8E93]" />
                  {selectedArticle.tags.map((tag, i) => (
                    <span key={i} className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-[#F2F3F5] text-[#45515E] border border-[#E5E7EB]">
                      {tag}
                    </span>
                  ))}
                </div>
              )}

              {/* Summary / Description */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-[#0A0A0A] uppercase tracking-wider">Summary</h3>
                <p className="text-sm text-[#45515E] leading-relaxed">
                  {selectedArticle.description}
                </p>
              </div>

              {/* Key Points */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-[#0A0A0A] uppercase tracking-wider">Key Points</h3>
                <div className="space-y-2">
                  {(selectedArticle.key_points || _generateKeyPoints(selectedArticle)).map((point, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-sm text-[#45515E]">
                      <span className="text-emerald-500 font-bold shrink-0 mt-0.5">•</span>
                      <span>{point}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Technical Context */}
              <div className="p-4 rounded-2xl bg-gradient-to-br from-[#F7F8FA] to-white border border-[#E5E7EB] space-y-2">
                <h4 className="text-xs font-bold text-[#0A0A0A] uppercase tracking-wider">Why This Matters</h4>
                <p className="text-xs text-[#45515E] leading-relaxed">
                  This article is relevant to your <strong>{newsData?.user_course || "technical"}</strong> learning path.
                  Staying up to date with {selectedArticle.category || "technical"} developments strengthens
                  your professional knowledge and interview readiness.
                </p>
              </div>

              {/* External Link */}
              {selectedArticle.url && (
                <div className="pt-4 border-t border-[#E5E7EB] flex justify-center">
                  <a
                    href={selectedArticle.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#0A0A0A] text-white font-semibold text-sm hover:bg-[#222] transition-colors"
                  >
                    <span>Read Original Source</span>
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Helper: generate key points from article description when not provided by API
function _generateKeyPoints(article) {
  const desc = article.description || "";
  const title = article.title || "";
  const cat = article.category || "Tech";

  return [
    `${cat} industry update covering the latest developments and best practices.`,
    desc.length > 80 ? desc.substring(0, 80) + "..." : desc,
    `Relevant to professionals working with ${(article.tags || []).slice(0, 3).join(", ") || cat} technologies.`,
  ].filter(p => p.length > 5);
}
