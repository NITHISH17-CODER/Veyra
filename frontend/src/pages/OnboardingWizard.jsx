import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { availableSkillsList } from '../constants/skillsData';
import { onboardingService } from '../services/onboardingService';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import {
  Sparkles,
  ArrowRight,
  ArrowLeft,
  Check,
  Upload,
  FileText,
  AlertCircle,
  FolderGit2,
  GraduationCap,
  Briefcase,
  Search,
  CheckCircle2
} from 'lucide-react';

const PROFICIENCY_LEVELS = [
  { value: "Beginner", num: 1 },
  { value: "Basic", num: 2 },
  { value: "Intermediate", num: 3 },
  { value: "Advanced", num: 4 },
  { value: "Expert", num: 5 }
];

export const OnboardingWizard = () => {
  const { user, submitOnboardingData } = useApp();
  const navigate = useNavigate();

  // Onboarding Sub-steps: 1: Name, 2: Journey/Background, 3: Details (Grad vs Job Seeker), 4: Skills & Preferences, 5: Profile Analysis
  const [step, setStep] = useState(1);

  // User State
  const [fullName, setFullName] = useState(user?.name || "");
  const [currentLevel, setCurrentLevel] = useState("graduation"); // 'graduation' | 'job_seeker'

  // Graduation Flow State
  const [degree, setDegree] = useState("B.Tech");
  const [branch, setBranch] = useState("Computer Science");
  const [college, setCollege] = useState("");
  const [stateName, setStateName] = useState("");
  const [district, setDistrict] = useState("");
  const [passedOutYear, setPassedOutYear] = useState(new Date().getFullYear().toString());
  const [naturalGoal, setNaturalGoal] = useState("");

  // Job Seeker Flow State
  const [targetRole, setTargetRole] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeStatus, setResumeStatus] = useState("idle"); // 'idle' | 'uploading' | 'done' | 'error'
  const [resumeAnalysis, setResumeAnalysis] = useState(null);
  const [githubUrl, setGithubUrl] = useState("");
  const [githubStatus, setGithubStatus] = useState("idle");
  const [githubData, setGithubData] = useState(null);
  const [linkedinUrl, setLinkedinUrl] = useState("");

  // Skills
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [skillSearch, setSkillSearch] = useState("");

  // AI Analysis State
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [aiMatchResult, setAiMatchResult] = useState(null);
  const [formError, setFormError] = useState("");

  // Restore status and protect against direct URL step skipping
  useEffect(() => {
    onboardingService.getOnboardingStatus()
      .then(res => {
        if (res.profile) {
          if (res.profile.full_name) setFullName(res.profile.full_name);
          if (res.profile.current_level) setCurrentLevel(res.profile.current_level);
          if (res.profile.degree) setDegree(res.profile.degree);
          if (res.profile.branch) setBranch(res.profile.branch);
          if (res.profile.college) setCollege(res.profile.college);
          if (res.profile.passed_out_year) setPassedOutYear(res.profile.passed_out_year.toString());
          if (res.profile.target_role) setTargetRole(res.profile.target_role);
          if (res.profile.career_goal) setNaturalGoal(res.profile.career_goal);
        }
        if (res.max_allowed_step) {
          setStep(Math.min(step, res.max_allowed_step));
        }
      })
      .catch(() => {});
  }, []);

  const handleStep1Continue = async () => {
    setFormError("");
    if (!fullName || fullName.trim().length < 2) {
      setFormError("Full Name is required and must be at least 2 characters.");
      return;
    }
    try {
      await onboardingService.saveOnboardingStep({ step: 1, full_name: fullName.trim() });
      setStep(2);
    } catch (err) {
      setFormError(err.response?.data?.detail || "Validation failed for Step 1.");
    }
  };

  const handleStep2Continue = async () => {
    setFormError("");
    if (!currentLevel) {
      setFormError("Please select your current standing (Graduation or Job Seeker).");
      return;
    }
    try {
      await onboardingService.saveOnboardingStep({ step: 2, current_level: currentLevel });
      setStep(3);
    } catch (err) {
      setFormError(err.response?.data?.detail || "Validation failed for Step 2.");
    }
  };

  const handleStep3Continue = async () => {
    setFormError("");
    if (currentLevel === "graduation") {
      if (!degree.trim() || !branch.trim() || !college.trim() || !naturalGoal.trim()) {
        setFormError("Please fill in degree, branch, college, and your target achievement goal.");
        return;
      }
    } else {
      if (!targetRole.trim()) {
        setFormError("Please enter your target role.");
        return;
      }
    }

    try {
      await onboardingService.saveOnboardingStep({
        step: 3,
        current_level: currentLevel,
        degree: degree.trim(),
        branch: branch.trim(),
        college: college.trim(),
        passed_out_year: parseInt(passedOutYear) || undefined,
        natural_goal: naturalGoal.trim(),
        target_role: targetRole.trim()
      });
      setStep(4);
    } catch (err) {
      setFormError(err.response?.data?.detail || "Validation failed for Step 3.");
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.match(/\.(pdf|docx|doc|txt)$/i)) {
      setFormError("Please upload a valid PDF or DOCX file.");
      return;
    }

    setResumeFile(file);
    setResumeStatus("uploading");
    setFormError("");

    try {
      const res = await onboardingService.uploadResume(file);
      setResumeAnalysis(res.analysis);
      setResumeStatus("done");

      if (res.analysis?.skills) {
        const extracted = res.analysis.skills;
        setSelectedSkills(prev => {
          const merged = [...prev];
          extracted.forEach(sk => {
            if (!merged.some(m => m.name.toLowerCase() === sk.name.toLowerCase())) {
              merged.push({
                name: sk.name,
                proficiency: "Intermediate",
                proficiency_num: sk.proficiency || 3,
                source: "resume"
              });
            }
          });
          return merged;
        });
      }
    } catch (err) {
      setResumeStatus("error");
      setFormError("Failed to analyze resume.");
    }
  };

  const handleAnalyzeGithub = async () => {
    if (!githubUrl.trim() || !githubUrl.includes("github.com/")) {
      setFormError("Please enter a valid GitHub profile URL.");
      return;
    }

    setGithubStatus("analyzing");
    setFormError("");

    try {
      const res = await onboardingService.analyzeGithub(githubUrl.trim());
      setGithubData(res.data);
      setGithubStatus("done");

      if (res.data?.extracted_skills) {
        const extracted = res.data.extracted_skills;
        setSelectedSkills(prev => {
          const merged = [...prev];
          extracted.forEach(sk => {
            if (!merged.some(m => m.name.toLowerCase() === sk.name.toLowerCase())) {
              merged.push({
                name: sk.name,
                proficiency: "Intermediate",
                proficiency_num: 3,
                source: "github"
              });
            }
          });
          return merged;
        });
      }
    } catch (err) {
      setGithubStatus("error");
      setFormError("Could not access GitHub profile.");
    }
  };

  const handleAddSkill = (skillName) => {
    if (!selectedSkills.some(s => s.name.toLowerCase() === skillName.toLowerCase())) {
      setSelectedSkills([
        ...selectedSkills,
        { name: skillName, proficiency: "Intermediate", proficiency_num: 3, source: "manual" }
      ]);
    }
    setSkillSearch("");
  };

  const handleRemoveSkill = (skillName) => {
    setSelectedSkills(selectedSkills.filter(s => s.name !== skillName));
  };

  const handleStartAnalysis = async () => {
    setIsAnalyzing(true);
    setFormError("");

    const effectiveGoal = currentLevel === "job_seeker" ? targetRole : (naturalGoal || "Software Engineering");

    const payload = {
      current_level: currentLevel,
      full_name: fullName.trim(),
      education: currentLevel === "graduation" ? degree : undefined,
      field_of_study: currentLevel === "graduation" ? branch.trim() : targetRole.trim(),
      college: college.trim() || undefined,
      state: stateName.trim() || undefined,
      district: district.trim() || undefined,
      passed_out_year: parseInt(passedOutYear) || undefined,
      target_role: targetRole.trim() || undefined,
      resume_url: resumeAnalysis ? `/uploads/resumes/${resumeFile?.name}` : undefined,
      github_url: githubUrl.trim() || undefined,
      linkedin_url: linkedinUrl.trim() || undefined,
      career_goal: effectiveGoal,
      skills: selectedSkills.map(s => ({
        name: s.name,
        proficiency: s.proficiency_num || 3
      }))
    };

    try {
      const result = await submitOnboardingData(payload);
      setAiMatchResult(result);
      setIsAnalyzing(false);
      setStep(5);
    } catch (err) {
      setIsAnalyzing(false);
      setFormError("Failed to complete profile analysis. Please check your data.");
    }
  };

  const handleFinishOnboarding = () => {
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-[#F7F8FA] flex flex-col justify-between p-4 sm:p-8 font-sans">
      {/* Header Bar */}
      <header className="max-w-3xl mx-auto w-full flex items-center justify-between py-4">
        <div className="flex items-center gap-2">
          <img
            src="/veyra-logo.png"
            alt="Veyra Logo"
            className="w-7 h-7 rounded-lg object-contain shadow-sm border border-[#1456F0]/20 shrink-0"
          />
          <span className="text-base font-extrabold text-[#0A0A0A] tracking-tight">Veyra</span>
        </div>

        {step <= 4 && (
          <span className="text-xs font-semibold text-[#8E8E93] bg-white px-3 py-1 rounded-full border border-[#E5E7EB]">
            0{step} / 05
          </span>
        )}
      </header>

      {/* Conversational Card */}
      <main className="max-w-2xl mx-auto w-full bg-white rounded-[24px] border border-[#E5E7EB] p-8 sm:p-12 my-auto space-y-8">
        {formError && (
          <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{formError}</span>
          </div>
        )}

        {/* STEP 1: Name */}
        {step === 1 && (
          <div className="space-y-8">
            <div className="space-y-2">
              <span className="text-xs font-semibold text-[#8E8E93] uppercase tracking-wider block">Step 01</span>
              <h1 className="text-3xl sm:text-4xl font-bold text-[#0A0A0A] tracking-tight">Let's start with you.</h1>
              <p className="text-sm text-[#45515E]">What should we call you?</p>
            </div>

            <div className="space-y-4">
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Full Name"
                className="input-flat w-full text-base py-3"
                autoFocus
              />

              <div className="flex justify-end pt-4">
                <Button
                  variant="primary"
                  size="lg"
                  disabled={!fullName.trim()}
                  icon={ArrowRight}
                  iconPosition="right"
                  onClick={handleStep1Continue}
                >
                  Continue
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* STEP 2: Background Screen */}
        {step === 2 && (
          <div className="space-y-8">
            <div className="space-y-2">
              <span className="text-xs font-semibold text-[#8E8E93] uppercase tracking-wider block">Step 02</span>
              <h1 className="text-3xl sm:text-4xl font-bold text-[#0A0A0A] tracking-tight">Where are you in your journey?</h1>
              <p className="text-sm text-[#45515E]">Select your current standing to tailor your path.</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div
                onClick={() => setCurrentLevel("graduation")}
                className={`p-6 rounded-2xl border cursor-pointer transition-all space-y-3 ${
                  currentLevel === "graduation"
                    ? 'border-[#0A0A0A] bg-[#F7F8FA] ring-1 ring-[#0A0A0A]'
                    : 'border-[#E5E7EB] bg-white hover:border-[#0A0A0A]'
                }`}
              >
                <div className="p-3 rounded-xl bg-white border border-[#E5E7EB] w-fit text-[#0A0A0A]">
                  <GraduationCap className="w-6 h-6" />
                </div>
                <div className="space-y-1">
                  <h3 className="text-lg font-bold text-[#0A0A0A]">GRADUATION</h3>
                  <p className="text-xs text-[#45515E]">Building your foundation and planning your career.</p>
                </div>
              </div>

              <div
                onClick={() => setCurrentLevel("job_seeker")}
                className={`p-6 rounded-2xl border cursor-pointer transition-all space-y-3 ${
                  currentLevel === "job_seeker"
                    ? 'border-[#0A0A0A] bg-[#F7F8FA] ring-1 ring-[#0A0A0A]'
                    : 'border-[#E5E7EB] bg-white hover:border-[#0A0A0A]'
                }`}
              >
                <div className="p-3 rounded-xl bg-white border border-[#E5E7EB] w-fit text-[#0A0A0A]">
                  <Briefcase className="w-6 h-6" />
                </div>
                <div className="space-y-1">
                  <h3 className="text-lg font-bold text-[#0A0A0A]">LOOKING FOR A JOB</h3>
                  <p className="text-xs text-[#45515E]">Ready to turn your skills into your next opportunity.</p>
                </div>
              </div>
            </div>

            <div className="flex justify-between pt-4">
              <Button variant="ghost" size="md" icon={ArrowLeft} onClick={() => setStep(1)}>
                Back
              </Button>
              <Button
                variant="primary"
                size="lg"
                icon={ArrowRight}
                iconPosition="right"
                onClick={handleStep2Continue}
              >
                Continue
              </Button>
            </div>
          </div>
        )}

        {/* STEP 3: Flow Details */}
        {step === 3 && (
          <div className="space-y-8">
            {currentLevel === "graduation" ? (
              <div className="space-y-6">
                <div className="space-y-2">
                  <span className="text-xs font-semibold text-[#8E8E93] uppercase tracking-wider block">Step 03</span>
                  <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">Academic Details &amp; Goal</h1>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <input
                    type="text"
                    value={degree}
                    onChange={(e) => setDegree(e.target.value)}
                    placeholder="Degree (e.g. B.Tech)"
                    className="input-flat"
                  />
                  <input
                    type="text"
                    value={branch}
                    onChange={(e) => setBranch(e.target.value)}
                    placeholder="Branch (e.g. Computer Science)"
                    className="input-flat"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <input
                    type="text"
                    value={college}
                    onChange={(e) => setCollege(e.target.value)}
                    placeholder="College"
                    className="input-flat col-span-2"
                  />
                  <input
                    type="text"
                    value={passedOutYear}
                    onChange={(e) => setPassedOutYear(e.target.value)}
                    placeholder="Passed Out Year"
                    className="input-flat"
                  />
                </div>

                <div className="space-y-2 pt-2">
                  <label className="text-sm font-semibold text-[#0A0A0A]">What do you want to achieve?</label>
                  <textarea
                    rows={3}
                    value={naturalGoal}
                    onChange={(e) => setNaturalGoal(e.target.value)}
                    placeholder="e.g. Become a Frontend Developer / Become a Backend Developer..."
                    className="input-flat w-full"
                  />
                  <div className="flex flex-wrap gap-2 pt-1">
                    {[
                      "Become a Frontend Developer",
                      "Become a Backend Developer",
                      "Become a Cybersecurity Professional",
                      "Become a Software Development Engineer",
                      "Become an AI Engineer"
                    ].map(ex => (
                      <button
                        key={ex}
                        type="button"
                        onClick={() => setNaturalGoal(ex)}
                        className="px-3 py-1 rounded-full border border-[#E5E7EB] text-xs font-medium text-[#45515E] hover:border-[#0A0A0A]"
                      >
                        {ex}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="space-y-2">
                  <span className="text-xs font-semibold text-[#8E8E93] uppercase tracking-wider block">Step 03</span>
                  <h1 className="text-2xl sm:text-3xl font-bold text-[#0A0A0A] tracking-tight">Let's understand your professional profile.</h1>
                </div>

                {/* Minimal Resume Upload */}
                <div className="p-6 rounded-2xl border border-[#E5E7EB] bg-[#F7F8FA] text-center space-y-3">
                  <FileText className="w-8 h-8 mx-auto text-[#0A0A0A]" />
                  <div>
                    <p className="text-sm font-bold text-[#0A0A0A]">Upload your resume</p>
                    <p className="text-xs text-[#8E8E93]">PDF or DOCX</p>
                  </div>

                  <label className="btn-pill-secondary text-xs inline-block cursor-pointer">
                    <span>{resumeFile ? resumeFile.name : "Choose File"}</span>
                    <input
                      type="file"
                      accept=".pdf,.docx,.doc,.txt"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                  </label>
                  {resumeStatus === 'done' && <p className="text-xs text-[#1BA673] font-semibold">Resume analyzed ✓</p>}
                </div>

                {/* GitHub & LinkedIn */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <input
                    type="url"
                    value={githubUrl}
                    onChange={(e) => setGithubUrl(e.target.value)}
                    placeholder="GitHub URL"
                    className="input-flat"
                  />
                  <input
                    type="url"
                    value={linkedinUrl}
                    onChange={(e) => setLinkedinUrl(e.target.value)}
                    placeholder="LinkedIn URL"
                    className="input-flat"
                  />
                </div>

                {/* Target Role */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-[#0A0A0A]">Which role are you targeting?</label>
                  <input
                    type="text"
                    value={targetRole}
                    onChange={(e) => setTargetRole(e.target.value)}
                    placeholder="e.g. Backend Developer"
                    className="input-flat w-full"
                  />
                </div>
              </div>
            )}

            <div className="flex justify-between pt-4">
              <Button variant="ghost" size="md" icon={ArrowLeft} onClick={() => setStep(2)}>
                Back
              </Button>
              <Button
                variant="primary"
                size="lg"
                icon={ArrowRight}
                iconPosition="right"
                onClick={handleStep3Continue}
              >
                Continue
              </Button>
            </div>
          </div>
        )}

        {/* STEP 4: Skills & Confirm */}
        {step === 4 && (
          <div className="space-y-8">
            <div className="space-y-2">
              <span className="text-xs font-semibold text-[#8E8E93] uppercase tracking-wider block">Step 04</span>
              <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">Your Current Skills</h1>
              <p className="text-sm text-[#45515E]">Add any additional skills you know.</p>
            </div>

            <div className="relative">
              <input
                type="text"
                value={skillSearch}
                onChange={(e) => setSkillSearch(e.target.value)}
                placeholder="Search skills (e.g. JavaScript, Python, SQL)..."
                className="input-flat w-full"
              />
              {skillSearch && (
                <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-[#E5E7EB] rounded-xl max-h-40 overflow-y-auto z-30 p-2 shadow-floating space-y-1">
                  {availableSkillsList
                    .filter(s => s.toLowerCase().includes(skillSearch.toLowerCase()))
                    .map(s => (
                      <div
                        key={s}
                        onClick={() => handleAddSkill(s)}
                        className="px-3 py-1.5 rounded-lg text-xs font-medium text-[#0A0A0A] hover:bg-[#F7F8FA] cursor-pointer flex justify-between"
                      >
                        <span>{s}</span>
                        <span className="font-bold">+ Add</span>
                      </div>
                    ))}
                </div>
              )}
            </div>

            {/* Selected Skills Chips */}
            <div className="flex flex-wrap gap-2">
              {selectedSkills.map(s => (
                <div key={s.name} className="px-3 py-1.5 rounded-full bg-[#F7F8FA] border border-[#E5E7EB] text-xs font-semibold text-[#0A0A0A] flex items-center gap-2">
                  <span>{s.name}</span>
                  <button onClick={() => handleRemoveSkill(s.name)} className="text-[#8E8E93] hover:text-rose-500 font-bold">×</button>
                </div>
              ))}
            </div>

            <div className="flex justify-between pt-4">
              <Button variant="ghost" size="md" icon={ArrowLeft} onClick={() => setStep(3)}>
                Back
              </Button>
              <Button
                variant="primary"
                size="lg"
                icon={Sparkles}
                iconPosition="right"
                onClick={handleStartAnalysis}
              >
                Analyze Profile
              </Button>
            </div>
          </div>
        )}

        {/* LOADING STATE */}
        {isAnalyzing && (
          <div className="py-12 text-center space-y-4">
            <div className="w-12 h-12 rounded-full bg-[#0A0A0A] text-white mx-auto flex items-center justify-center animate-spin">
              <Sparkles className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-[#0A0A0A]">Analyzing Profile...</h3>
          </div>
        )}

        {/* STEP 5: PROFILE ANALYSIS SCREEN */}
        {step === 5 && !isAnalyzing && (
          <div className="space-y-8">
            <div className="space-y-2">
              <span className="text-xs font-semibold text-[#8E8E93] uppercase tracking-wider block">PROFILE ANALYSIS</span>
              <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">Here's what we understood.</h1>
            </div>

            {/* Summary List */}
            <div className="p-6 rounded-2xl bg-[#F7F8FA] border border-[#E5E7EB] space-y-4 text-sm">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="text-xs text-[#8E8E93] block">Background</span>
                  <span className="font-semibold text-[#0A0A0A] capitalize">{currentLevel === 'graduation' ? `${degree} in ${branch}` : 'Job Seeker'}</span>
                </div>
                <div>
                  <span className="text-xs text-[#8E8E93] block">Goal</span>
                  <span className="font-semibold text-[#0A0A0A]">{targetRole || naturalGoal || "Software Engineering"}</span>
                </div>
              </div>

              <div className="pt-3 border-t border-[#E5E7EB] flex flex-wrap gap-4 text-xs font-medium text-[#45515E]">
                <span>Resume {resumeStatus === 'done' ? '✓' : '—'}</span>
                <span>GitHub {githubStatus === 'done' ? '✓' : '—'}</span>
                <span>LinkedIn {linkedinUrl ? '✓' : '—'}</span>
              </div>
            </div>

            {/* Recommended Focus Section */}
            <div className="space-y-3">
              <h3 className="text-base font-bold text-[#0A0A0A]">Recommended Focus</h3>
              <div className="space-y-2">
                {[
                  { name: "Java", pct: "92%" },
                  { name: "Spring Boot", pct: "86%" },
                  { name: "REST APIs", pct: "81%" },
                  { name: "SQL", pct: "74%" },
                  { name: "Testing", pct: "61%" }
                ].map((item, idx) => (
                  <div key={item.name} className="flex items-center justify-between p-3 rounded-xl border border-[#E5E7EB] bg-white text-xs font-semibold">
                    <span className="text-[#0A0A0A]">0{idx + 1} {item.name}</span>
                    <span className="font-mono text-[#45515E]">{item.pct}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Your Recommended Path */}
            <div className="p-6 rounded-2xl bg-[#0A0A0A] text-white space-y-3">
              <span className="text-xs font-semibold tracking-wider uppercase text-[#8E8E93]">Your recommended path</span>
              <h3 className="text-xl font-bold text-white">
                {aiMatchResult?.matched_careers?.[0]?.career || targetRole || "Backend Developer"}
              </h3>
              <p className="text-xs text-[#8E8E93] leading-relaxed">
                {aiMatchResult?.matched_careers?.[0]?.why_recommended || "Curated based on your educational background, declared skills, and targeted technical competencies."}
              </p>
            </div>

            <div className="flex flex-col sm:flex-row items-center gap-3 pt-4">
              <Button
                variant="primary"
                size="lg"
                icon={ArrowRight}
                iconPosition="right"
                onClick={handleFinishOnboarding}
                className="w-full justify-center"
              >
                Start My Learning Path
              </Button>
              <Button
                variant="outline"
                size="lg"
                onClick={() => setStep(3)}
                className="w-full justify-center"
              >
                Change Goal
              </Button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};
