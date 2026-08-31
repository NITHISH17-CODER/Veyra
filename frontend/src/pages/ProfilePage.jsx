import React, { useState, useEffect, useRef } from 'react';
import { useApp } from '../context/AppContext';
import { profileService } from '../services/profileService';
import { skillService } from '../services/skillService';
import { API_BASE_URL } from '../services/api';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { SkillChip } from '../components/common/SkillChip';
import {
  Check,
  Edit2,
  Camera,
  Trash2,
  Plus,
  RotateCcw,
  FileText,
  AlertCircle,
  Clock,
  GraduationCap,
  Sparkles,
  X,
  Search,
  Sliders
} from 'lucide-react';

const backendOrigin = API_BASE_URL.replace(/\/api\/?$/, '');

const GithubIcon = ({ className = "w-4 h-4" }) => (
  <svg className={className} fill="currentColor" viewBox="0 0 24 24">
    <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
  </svg>
);

const LinkedinIcon = ({ className = "w-4 h-4" }) => (
  <svg className={className} fill="currentColor" viewBox="0 0 24 24">
    <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z" />
  </svg>
);

const PROFICIENCY_OPTIONS = [
  { value: 1, label: 'Beginner' },
  { value: 2, label: 'Basic' },
  { value: 3, label: 'Intermediate' },
  { value: 4, label: 'Advanced' },
  { value: 5, label: 'Expert' }
];

const DEFAULT_POPULAR_SKILLS = [
  "JavaScript", "Python", "React", "HTML & CSS", "Node.js", "Java", "SQL", "Git", "Docker", "TypeScript", "FastAPI", "C++"
];

export const ProfilePage = () => {
  const { user, refreshUserData, showToast, updateUserGoal, generateNewPath } = useApp();

  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [loadingRecalc, setLoadingRecalc] = useState(false);

  // Form Fields
  const [fullName, setFullName] = useState(user?.name || '');
  const [careerGoal, setCareerGoal] = useState(user?.targetGoal || '');
  const [degree, setDegree] = useState(user?.education || '');
  const [branch, setBranch] = useState(user?.fieldOfStudy || '');
  const [college, setCollege] = useState(user?.college || '');
  const [state, setState] = useState(user?.state || '');
  const [district, setDistrict] = useState(user?.district || '');
  const [passedOutYear, setPassedOutYear] = useState(user?.passedOutYear || '');
  const [learningHours, setLearningHours] = useState(user?.weeklyGoalHours || 10);

  // Skills
  const [skills, setSkills] = useState(user?.skills || []);
  const [showAddSkillModal, setShowAddSkillModal] = useState(false);
  const [newSkillName, setNewSkillName] = useState('');
  const [newSkillProficiency, setNewSkillProficiency] = useState(3);
  const [masterSkills, setMasterSkills] = useState([]);
  const [editingSkill, setEditingSkill] = useState(null); // { id, name, proficiency_val }

  // Profile Photo state
  const [photoLoading, setPhotoLoading] = useState(false);
  const fileInputRef = useRef(null);

  // Evidence Verification States
  const [githubInput, setGithubInput] = useState(user?.githubUrl || '');
  const [editingGithub, setEditingGithub] = useState(false);
  const [githubLoading, setGithubLoading] = useState(false);

  const [linkedinInput, setLinkedinInput] = useState(user?.linkedinUrl || '');
  const [editingLinkedin, setEditingLinkedin] = useState(false);
  const [linkedinLoading, setLinkedinLoading] = useState(false);

  const [resumeLoading, setResumeLoading] = useState(false);
  const resumeInputRef = useRef(null);

  // Sync state when user prop updates
  useEffect(() => {
    if (user) {
      setFullName(user.name || '');
      setCareerGoal(user.targetGoal || '');
      setDegree(user.education || '');
      setBranch(user.fieldOfStudy || '');
      setCollege(user.college || '');
      setState(user.state || '');
      setDistrict(user.district || '');
      setPassedOutYear(user.passedOutYear || '');
      setLearningHours(user.weeklyGoalHours || 10);
      setSkills(user.skills || []);
      setGithubInput(user.githubUrl || '');
      setLinkedinInput(user.linkedinUrl || '');
    }
  }, [user]);

  // Load master catalog skills for suggestions
  useEffect(() => {
    skillService.getAvailableSkills()
      .then(res => {
        if (Array.isArray(res)) {
          setMasterSkills(res.map(s => s.name));
        }
      })
      .catch(() => {});
  }, []);

  // Photo handlers
  const handlePhotoUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
    if (!allowedTypes.includes(file.type.toLowerCase())) {
      showToast('Invalid file format. Please select a JPG, PNG, WebP, or GIF image.', 'error');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      showToast('Photo size exceeds 5MB limit.', 'error');
      return;
    }

    try {
      setPhotoLoading(true);
      const formData = new FormData();
      formData.append('file', file);
      await profileService.uploadPhoto(formData);
      await refreshUserData();
      showToast('Profile photo updated successfully!', 'success');
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to upload profile photo.', 'error');
    } finally {
      setPhotoLoading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handlePhotoRemove = async () => {
    try {
      setPhotoLoading(true);
      await profileService.removePhoto();
      await refreshUserData();
      showToast('Profile photo removed.', 'info');
    } catch (err) {
      showToast('Failed to remove profile photo.', 'error');
    } finally {
      setPhotoLoading(false);
    }
  };

  // Skill Inventory Handlers
  const handleAddSkill = async () => {
    const cleanName = newSkillName.trim();
    if (!cleanName) {
      showToast('Please select or type a valid skill name.', 'warning');
      return;
    }

    // Check duplicate
    const existing = skills.find(s => s.name?.toLowerCase() === cleanName.toLowerCase());
    if (existing) {
      showToast(`Skill '${cleanName}' is already in your inventory. You can edit its level below.`, 'info');
      setEditingSkill({
        id: existing.id,
        name: existing.name,
        proficiency_val: existing.proficiency_val || 3
      });
      setShowAddSkillModal(false);
      return;
    }

    try {
      await skillService.addUserSkill(null, Number(newSkillProficiency), cleanName);
      await refreshUserData();
      setNewSkillName('');
      setNewSkillProficiency(3);
      setShowAddSkillModal(false);
      showToast(`Skill '${cleanName}' added to your profile!`, 'success');
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to add skill.', 'error');
    }
  };

  const handleUpdateSkillProficiency = async (userSkillId, newProfVal) => {
    try {
      await skillService.updateUserSkill(userSkillId, Number(newProfVal));
      await refreshUserData();
      setEditingSkill(null);
      showToast('Skill proficiency updated successfully!', 'success');
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to update skill proficiency.', 'error');
    }
  };

  const handleRemoveSkill = async (userSkillId, name) => {
    try {
      if (userSkillId) {
        await skillService.deleteUserSkill(userSkillId);
      }
      await refreshUserData();
      showToast(`Skill '${name}' removed.`, 'info');
    } catch (err) {
      showToast('Failed to remove skill.', 'error');
    }
  };

  // Main Profile Save Flow
  const handleSaveChanges = async () => {
    try {
      setSaving(true);
      const payload = {
        full_name: fullName.trim(),
        career_goal: careerGoal.trim(),
        education: degree.trim(),
        field_of_study: branch.trim(),
        college: college.trim(),
        state: state.trim(),
        district: district.trim(),
        passed_out_year: passedOutYear ? Number(passedOutYear) : null,
        learning_hours_per_week: Number(learningHours),
      };

      await profileService.updateProfile(payload);
      await refreshUserData();
      setIsEditing(false);
      showToast('Profile changes saved to database successfully!', 'success');
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to save profile changes.', 'error');
    } finally {
      setSaving(false);
    }
  };

  // Recalculate Roadmap Goal
  const handleRecalculateGoal = async () => {
    if (!careerGoal.trim()) {
      showToast('Please enter a career goal.', 'warning');
      return;
    }
    setLoadingRecalc(true);
    try {
      await updateUserGoal(careerGoal.trim());
      await generateNewPath(careerGoal.trim(), skills);
      showToast('Target goal updated and roadmap regenerated!', 'success');
    } catch (err) {
      showToast('Could not regenerate roadmap for new goal.', 'warning');
    } finally {
      setLoadingRecalc(false);
    }
  };

  // Verification Handlers
  const handleVerifyGithub = async () => {
    if (!githubInput.trim()) {
      showToast('Please enter a GitHub URL.', 'warning');
      return;
    }
    try {
      setGithubLoading(true);
      const res = await profileService.verifyGithub(githubInput.trim());
      await refreshUserData();
      setEditingGithub(false);
      if (res.github_status === 'connected') {
        showToast('✓ GitHub Profile verified & connected successfully!', 'success');
      } else {
        showToast(`✕ GitHub Verification Failed: ${res.github_error || 'Invalid profile.'}`, 'error');
      }
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to verify GitHub URL.', 'error');
    } finally {
      setGithubLoading(false);
    }
  };

  const handleVerifyLinkedin = async () => {
    if (!linkedinInput.trim()) {
      showToast('Please enter a LinkedIn profile URL.', 'warning');
      return;
    }
    try {
      setLinkedinLoading(true);
      const res = await profileService.verifyLinkedin(linkedinInput.trim());
      await refreshUserData();
      setEditingLinkedin(false);
      if (res.linkedin_status === 'connected') {
        showToast('✓ LinkedIn Profile verified & connected successfully!', 'success');
      } else {
        showToast(`✕ LinkedIn Verification Failed: ${res.linkedin_error || 'Invalid URL.'}`, 'error');
      }
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to verify LinkedIn URL.', 'error');
    } finally {
      setLinkedinLoading(false);
    }
  };

  const handleResumeUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const allowedExts = ['.pdf', '.docx', '.doc', '.txt'];
    const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    if (!allowedExts.includes(ext)) {
      showToast('Invalid file format. Please upload a PDF, DOCX, or TXT file.', 'error');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      showToast('Resume size exceeds 10MB limit.', 'error');
      return;
    }

    try {
      setResumeLoading(true);
      const formData = new FormData();
      formData.append('file', file);
      const res = await profileService.uploadResume(formData);
      await refreshUserData();
      if (res.resume_status === 'verified') {
        showToast('✓ Resume uploaded, verified & analyzed by AI!', 'success');
      } else {
        showToast(`✕ Resume Verification Failed: ${res.resume_error || 'Could not analyze file.'}`, 'error');
      }
    } catch (err) {
      showToast(err.response?.data?.detail || 'Failed to upload and verify resume.', 'error');
    } finally {
      setResumeLoading(false);
      if (resumeInputRef.current) resumeInputRef.current.value = '';
    }
  };

  // Helper for photo URL
  const photoSrc = user?.avatar_url
    ? user.avatar_url.startsWith('http')
      ? user.avatar_url
      : `${backendOrigin}${user.avatar_url}`
    : null;

  // Filter skill suggestions
  const catalogList = masterSkills.length > 0 ? masterSkills : DEFAULT_POPULAR_SKILLS;
  const filteredSuggestions = catalogList
    .filter(s => s.toLowerCase().includes(newSkillName.toLowerCase().trim()))
    .filter(s => !skills.some(userSk => userSk.name?.toLowerCase() === s.toLowerCase()))
    .slice(0, 8);

  return (
    <div className="space-y-8 animate-fadeIn font-sans max-w-5xl mx-auto pb-12">
      {/* Hidden File Inputs */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handlePhotoUpload}
        accept="image/jpeg,image/png,image/webp,image/gif"
        className="hidden"
      />
      <input
        type="file"
        ref={resumeInputRef}
        onChange={handleResumeUpload}
        accept=".pdf,.docx,.doc,.txt"
        className="hidden"
      />

      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-[#E5E7EB] pb-6 gap-4">
        <div className="space-y-1">
          <span className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider">Veyra User Profile</span>
          <h1 className="text-3xl font-bold text-[#0A0A0A] tracking-tight">{user?.name || 'User Profile'}</h1>
        </div>

        <div className="flex items-center gap-3">
          {isEditing ? (
            <>
              <Button
                variant="outline"
                size="md"
                onClick={() => setIsEditing(false)}
                disabled={saving}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                size="md"
                icon={Check}
                loading={saving}
                onClick={handleSaveChanges}
              >
                Save Changes
              </Button>
            </>
          ) : (
            <Button
              variant="outline"
              size="md"
              icon={Edit2}
              onClick={() => setIsEditing(true)}
            >
              Edit Profile
            </Button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Photo & Evidence Overview */}
        <div className="lg:col-span-4 space-y-6">
          {/* Avatar Card */}
          <Card radius="24" className="p-6 text-center space-y-4 relative overflow-hidden">
            <div className="relative inline-block mx-auto group">
              {photoSrc ? (
                <img
                  src={photoSrc}
                  alt={user?.name}
                  className="w-28 h-28 rounded-full object-cover border-4 border-[#F3F4F6] shadow-sm mx-auto"
                />
              ) : (
                <div className="w-28 h-28 rounded-full bg-[#0A0A0A] text-white text-3xl font-bold flex items-center justify-center border-4 border-[#F3F4F6] shadow-sm mx-auto">
                  {user?.name ? user.name.substring(0, 2).toUpperCase() : 'PP'}
                </div>
              )}

              {photoLoading && (
                <div className="absolute inset-0 rounded-full bg-black/50 flex items-center justify-center text-white text-xs font-semibold">
                  Uploading...
                </div>
              )}
            </div>

            <div>
              <h2 className="text-xl font-bold text-[#0A0A0A]">{user?.name || 'User'}</h2>
              <span className="text-xs text-[#8E8E93]">{user?.email || 'user@veyra.ai'}</span>
            </div>

            {/* Photo Action Buttons */}
            <div className="pt-3 border-t border-[#E5E7EB] flex flex-wrap items-center justify-center gap-2">
              <Button
                variant="outline"
                size="sm"
                icon={Camera}
                loading={photoLoading}
                onClick={() => fileInputRef.current?.click()}
              >
                {photoSrc ? 'Replace Photo' : 'Upload Photo'}
              </Button>
              {photoSrc && (
                <Button
                  variant="ghost"
                  size="sm"
                  icon={Trash2}
                  loading={photoLoading}
                  onClick={handlePhotoRemove}
                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  Remove
                </Button>
              )}
            </div>

            <div className="pt-3 border-t border-[#E5E7EB]">
              <span className="text-xs font-semibold text-[#8E8E93]">Learning Progress Score</span>
              <span className="text-3xl font-bold text-[#1456F0] block font-mono mt-1">{user?.readinessScore || 0}%</span>
            </div>
          </Card>

          {/* Verification Evidence Overview */}
          <Card radius="24" className="p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-[#E5E7EB] pb-3">
              <h3 className="text-sm font-bold text-[#0A0A0A] flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#1456F0]" />
                Verification Evidence
              </h3>
              <span className="text-xs text-[#8E8E93]">Backend Validated</span>
            </div>

            {/* GitHub Verification Status */}
            <div className="space-y-2 p-3 rounded-xl bg-[#F9FAFB] border border-[#E5E7EB]">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-[#0A0A0A] flex items-center gap-1.5">
                  <GithubIcon className="w-4 h-4 text-[#0A0A0A]" /> GitHub
                </span>
                {user?.githubStatus === 'connected' ? (
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-green-100 text-green-800 flex items-center gap-1">
                    ✓ Connected
                  </span>
                ) : user?.githubStatus === 'failed' ? (
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-red-100 text-red-800 flex items-center gap-1">
                    ✕ Failed
                  </span>
                ) : (
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-gray-200 text-gray-700">
                    Not Connected
                  </span>
                )}
              </div>

              {user?.githubStatus === 'connected' && user?.githubUrl && (
                <p className="text-xs text-[#45515E] truncate">
                  <a href={user.githubUrl} target="_blank" rel="noreferrer" className="text-[#0066FF] hover:underline">
                    {user.githubUrl}
                  </a>
                </p>
              )}

              {user?.githubStatus === 'failed' && user?.githubError && (
                <p className="text-[11px] text-red-600 flex items-center gap-1">
                  <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                  {user.githubError}
                </p>
              )}

              {editingGithub ? (
                <div className="pt-2 space-y-2">
                  <input
                    type="url"
                    placeholder="https://github.com/username"
                    value={githubInput}
                    onChange={(e) => setGithubInput(e.target.value)}
                    className="w-full text-xs px-3 py-1.5 border border-[#D1D5DB] rounded-lg focus:outline-none focus:border-[#0A0A0A]"
                  />
                  <div className="flex justify-end gap-2">
                    <Button size="sm" variant="ghost" onClick={() => setEditingGithub(false)}>Cancel</Button>
                    <Button size="sm" variant="primary" loading={githubLoading} onClick={handleVerifyGithub}>
                      Verify &amp; Save
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="pt-1 text-right">
                  <button
                    onClick={() => setEditingGithub(true)}
                    className="text-xs font-semibold text-[#0066FF] hover:underline"
                  >
                    {user?.githubStatus === 'connected' ? 'Edit GitHub' : user?.githubStatus === 'failed' ? 'Retry Verification' : 'Connect GitHub'}
                  </button>
                </div>
              )}
            </div>

            {/* LinkedIn Verification Status */}
            <div className="space-y-2 p-3 rounded-xl bg-[#F9FAFB] border border-[#E5E7EB]">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-[#0A0A0A] flex items-center gap-1.5">
                  <LinkedinIcon className="w-4 h-4 text-[#0A66C2]" /> LinkedIn
                </span>
                {user?.linkedinStatus === 'connected' ? (
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-green-100 text-green-800 flex items-center gap-1">
                    ✓ Connected
                  </span>
                ) : user?.linkedinStatus === 'failed' ? (
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-red-100 text-red-800 flex items-center gap-1">
                    ✕ Failed
                  </span>
                ) : (
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-gray-200 text-gray-700">
                    Not Connected
                  </span>
                )}
              </div>

              {user?.linkedinStatus === 'connected' && user?.linkedinUrl && (
                <p className="text-xs text-[#45515E] truncate">
                  <a href={user.linkedinUrl} target="_blank" rel="noreferrer" className="text-[#0066FF] hover:underline">
                    {user.linkedinUrl}
                  </a>
                </p>
              )}

              {user?.linkedinStatus === 'failed' && user?.linkedinError && (
                <p className="text-[11px] text-red-600 flex items-center gap-1">
                  <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                  {user.linkedinError}
                </p>
              )}

              {editingLinkedin ? (
                <div className="pt-2 space-y-2">
                  <input
                    type="url"
                    placeholder="https://www.linkedin.com/in/username"
                    value={linkedinInput}
                    onChange={(e) => setLinkedinInput(e.target.value)}
                    className="w-full text-xs px-3 py-1.5 border border-[#D1D5DB] rounded-lg focus:outline-none focus:border-[#0A0A0A]"
                  />
                  <div className="flex justify-end gap-2">
                    <Button size="sm" variant="ghost" onClick={() => setEditingLinkedin(false)}>Cancel</Button>
                    <Button size="sm" variant="primary" loading={linkedinLoading} onClick={handleVerifyLinkedin}>
                      Verify &amp; Save
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="pt-1 text-right">
                  <button
                    onClick={() => setEditingLinkedin(true)}
                    className="text-xs font-semibold text-[#0066FF] hover:underline"
                  >
                    {user?.linkedinStatus === 'connected' ? 'Edit LinkedIn' : user?.linkedinStatus === 'failed' ? 'Retry Verification' : 'Connect LinkedIn'}
                  </button>
                </div>
              )}
            </div>

            {/* Resume Verification Status */}
            <div className="space-y-2 p-3 rounded-xl bg-[#F9FAFB] border border-[#E5E7EB]">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-[#0A0A0A] flex items-center gap-1.5">
                  <FileText className="w-4 h-4 text-[#E11D48]" /> Resume
                </span>
                {user?.resumeStatus === 'verified' ? (
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-green-100 text-green-800 flex items-center gap-1">
                    ✓ Verified &amp; Analyzed
                  </span>
                ) : user?.resumeStatus === 'failed' ? (
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-red-100 text-red-800 flex items-center gap-1">
                    ✕ Verification Failed
                  </span>
                ) : user?.resumeStatus === 'analyzing' ? (
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-blue-100 text-blue-800 animate-pulse">
                    Analyzing...
                  </span>
                ) : (
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-gray-200 text-gray-700">
                    Not Uploaded
                  </span>
                )}
              </div>

              {user?.resumeStatus === 'verified' && user?.resumeAnalysis?.skills?.length > 0 && (
                <div className="space-y-1 pt-1">
                  <span className="text-[11px] font-semibold text-[#8E8E93]">Extracted Tech:</span>
                  <div className="flex flex-wrap gap-1">
                    {user.resumeAnalysis.skills.slice(0, 4).map((sk, idx) => (
                      <span key={idx} className="text-[10px] px-2 py-0.5 bg-white border border-[#E5E7EB] rounded-full text-[#0A0A0A] font-medium">
                        {sk.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {user?.resumeStatus === 'failed' && user?.resumeError && (
                <p className="text-[11px] text-red-600 flex items-center gap-1">
                  <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                  {user.resumeError}
                </p>
              )}

              <div className="pt-1 text-right">
                <button
                  disabled={resumeLoading}
                  onClick={() => resumeInputRef.current?.click()}
                  className="text-xs font-semibold text-[#0066FF] hover:underline disabled:opacity-50"
                >
                  {resumeLoading
                    ? 'Uploading & Analyzing...'
                    : user?.resumeStatus === 'verified'
                    ? 'Replace Resume'
                    : user?.resumeStatus === 'failed'
                    ? 'Retry Verification'
                    : 'Upload Resume'}
                </button>
              </div>
            </div>
          </Card>
        </div>

        {/* Right Column: Detailed Editable Profile Information */}
        <div className="lg:col-span-8 space-y-6">
          <Card radius="24" className="p-6 space-y-6">
            {/* Full Name & Career Goal */}
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider block">Full Name</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      className="w-full text-sm font-semibold px-3 py-2 border border-[#D1D5DB] rounded-xl focus:outline-none focus:border-[#0A0A0A]"
                    />
                  ) : (
                    <p className="text-lg font-bold text-[#0A0A0A]">{user?.name || 'Not provided'}</p>
                  )}
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider block">Career Goal</label>
                  {isEditing ? (
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={careerGoal}
                        onChange={(e) => setCareerGoal(e.target.value)}
                        placeholder="e.g. AI Systems Engineer"
                        className="flex-1 text-sm font-semibold px-3 py-2 border border-[#D1D5DB] rounded-xl focus:outline-none focus:border-[#0A0A0A]"
                      />
                      <Button
                        variant="outline"
                        size="sm"
                        loading={loadingRecalc}
                        icon={RotateCcw}
                        onClick={handleRecalculateGoal}
                        title="Update Goal & Regenerate Roadmap"
                      >
                        Sync Roadmap
                      </Button>
                    </div>
                  ) : (
                    <p className="text-lg font-bold text-[#0A0A0A]">{user?.targetGoal || 'Not specified'}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Educational Details */}
            <div className="space-y-4 pt-5 border-t border-[#E5E7EB]">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider flex items-center gap-1.5">
                  <GraduationCap className="w-4 h-4 text-[#0A0A0A]" />
                  Educational Details
                </label>
              </div>

              {isEditing ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <span className="text-xs font-medium text-[#45515E]">Degree</span>
                    <input
                      type="text"
                      value={degree}
                      onChange={(e) => setDegree(e.target.value)}
                      placeholder="e.g. B.Tech / Bachelor of Science"
                      className="w-full text-xs px-3 py-2 border border-[#D1D5DB] rounded-xl focus:outline-none focus:border-[#0A0A0A]"
                    />
                  </div>

                  <div className="space-y-1">
                    <span className="text-xs font-medium text-[#45515E]">Branch / Major</span>
                    <input
                      type="text"
                      value={branch}
                      onChange={(e) => setBranch(e.target.value)}
                      placeholder="e.g. Computer Science & Engineering"
                      className="w-full text-xs px-3 py-2 border border-[#D1D5DB] rounded-xl focus:outline-none focus:border-[#0A0A0A]"
                    />
                  </div>

                  <div className="space-y-1">
                    <span className="text-xs font-medium text-[#45515E]">College / Institution</span>
                    <input
                      type="text"
                      value={college}
                      onChange={(e) => setCollege(e.target.value)}
                      placeholder="e.g. SRM Institute of Science and Technology"
                      className="w-full text-xs px-3 py-2 border border-[#D1D5DB] rounded-xl focus:outline-none focus:border-[#0A0A0A]"
                    />
                  </div>

                  <div className="space-y-1">
                    <span className="text-xs font-medium text-[#45515E]">Passed Out Year</span>
                    <input
                      type="number"
                      value={passedOutYear}
                      onChange={(e) => setPassedOutYear(e.target.value)}
                      placeholder="e.g. 2025"
                      className="w-full text-xs px-3 py-2 border border-[#D1D5DB] rounded-xl focus:outline-none focus:border-[#0A0A0A]"
                    />
                  </div>

                  <div className="space-y-1">
                    <span className="text-xs font-medium text-[#45515E]">State</span>
                    <input
                      type="text"
                      value={state}
                      onChange={(e) => setState(e.target.value)}
                      placeholder="e.g. Tamil Nadu"
                      className="w-full text-xs px-3 py-2 border border-[#D1D5DB] rounded-xl focus:outline-none focus:border-[#0A0A0A]"
                    />
                  </div>

                  <div className="space-y-1">
                    <span className="text-xs font-medium text-[#45515E]">District</span>
                    <input
                      type="text"
                      value={district}
                      onChange={(e) => setDistrict(e.target.value)}
                      placeholder="e.g. Chennai"
                      className="w-full text-xs px-3 py-2 border border-[#D1D5DB] rounded-xl focus:outline-none focus:border-[#0A0A0A]"
                    />
                  </div>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-[#F9FAFB] p-4 rounded-2xl border border-[#E5E7EB]">
                  <div>
                    <span className="text-[11px] font-bold text-[#8E8E93] uppercase block">Degree</span>
                    <p className="text-sm font-semibold text-[#0A0A0A]">{user?.education || 'Not specified'}</p>
                  </div>
                  <div>
                    <span className="text-[11px] font-bold text-[#8E8E93] uppercase block">Branch</span>
                    <p className="text-sm font-semibold text-[#0A0A0A]">{user?.fieldOfStudy || 'Not specified'}</p>
                  </div>
                  <div>
                    <span className="text-[11px] font-bold text-[#8E8E93] uppercase block">College</span>
                    <p className="text-sm font-semibold text-[#0A0A0A]">{user?.college || 'Not specified'}</p>
                  </div>
                  <div>
                    <span className="text-[11px] font-bold text-[#8E8E93] uppercase block">Passed Out Year</span>
                    <p className="text-sm font-semibold text-[#0A0A0A]">{user?.passedOutYear || 'Not specified'}</p>
                  </div>
                  {user?.state && (
                    <div>
                      <span className="text-[11px] font-bold text-[#8E8E93] uppercase block">State</span>
                      <p className="text-sm font-semibold text-[#0A0A0A]">{user.state}</p>
                    </div>
                  )}
                  {user?.district && (
                    <div>
                      <span className="text-[11px] font-bold text-[#8E8E93] uppercase block">District</span>
                      <p className="text-sm font-semibold text-[#0A0A0A]">{user.district}</p>
                    </div>
                  )}
                </div>
              )}

              {/* Available Learning Hours Display */}
              <div className="p-4 rounded-2xl bg-[#F0FDF4] border border-[#DCFCE7] flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-xl bg-green-600 text-white">
                    <Clock className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="text-xs font-bold text-green-900 uppercase tracking-wider block">Available Learning Hours</span>
                    <span className="text-sm text-green-800 font-semibold">Collected during Onboarding Step 5</span>
                  </div>
                </div>

                {isEditing ? (
                  <div className="flex items-center gap-2">
                    <input
                      type="number"
                      min="1"
                      max="168"
                      value={learningHours}
                      onChange={(e) => setLearningHours(e.target.value)}
                      className="w-20 text-sm font-bold text-center px-2 py-1.5 border border-green-300 rounded-lg focus:outline-none focus:border-green-600 bg-white"
                    />
                    <span className="text-xs font-bold text-green-900">hours/week</span>
                  </div>
                ) : (
                  <span className="text-lg font-bold text-green-900 font-mono">
                    {user?.weeklyGoalHours || 10} hours/week
                  </span>
                )}
              </div>
            </div>

            {/* Skill Inventory Component */}
            <div className="space-y-4 pt-5 border-t border-[#E5E7EB]">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-xs font-bold text-[#8E8E93] uppercase tracking-wider block">
                    Skill Inventory ({skills.length})
                  </label>
                  <span className="text-xs text-[#8E8E93]">Click any skill to edit its proficiency level</span>
                </div>
                <Button
                  size="sm"
                  variant="primary"
                  icon={Plus}
                  onClick={() => setShowAddSkillModal(true)}
                >
                  Add Skill
                </Button>
              </div>

              {/* Add Skill Modal / Selector */}
              {showAddSkillModal && (
                <div className="p-5 rounded-2xl bg-[#F9FAFB] border-2 border-[#0A0A0A]/10 space-y-4 animate-fadeIn shadow-sm">
                  <div className="flex items-center justify-between border-b border-[#E5E7EB] pb-3">
                    <h4 className="text-sm font-bold text-[#0A0A0A] flex items-center gap-2">
                      <Search className="w-4 h-4 text-[#0066FF]" />
                      Add Skill to Inventory
                    </h4>
                    <button onClick={() => setShowAddSkillModal(false)} className="text-[#8E8E93] hover:text-[#0A0A0A] p-1">
                      <X className="w-4 h-4" />
                    </button>
                  </div>

                  {/* 1. Search & Type Skill */}
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-[#45515E] block">1. Search or Type Skill Name</label>
                    <div className="relative">
                      <Search className="w-4 h-4 absolute left-3 top-3 text-[#9CA3AF]" />
                      <input
                        type="text"
                        placeholder="Search skills (e.g. JavaScript, Python, React)..."
                        value={newSkillName}
                        onChange={(e) => setNewSkillName(e.target.value)}
                        className="w-full text-sm pl-9 pr-3 py-2 border border-[#D1D5DB] rounded-xl focus:outline-none focus:border-[#0A0A0A] bg-white shadow-sm"
                      />
                    </div>

                    {/* Suggestions list */}
                    {filteredSuggestions.length > 0 && (
                      <div className="space-y-1 pt-1">
                        <span className="text-[11px] font-semibold text-[#8E8E93]">Suggested Skills:</span>
                        <div className="flex flex-wrap gap-1.5">
                          {filteredSuggestions.map((sug) => (
                            <button
                              key={sug}
                              type="button"
                              onClick={() => setNewSkillName(sug)}
                              className="text-xs px-2.5 py-1 bg-white hover:bg-[#F3F4F6] border border-[#E5E7EB] rounded-lg text-[#0A0A0A] font-medium transition-colors"
                            >
                              + {sug}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* 2. Select Proficiency Level */}
                  <div className="space-y-2 pt-2 border-t border-[#E5E7EB]">
                    <label className="text-xs font-bold text-[#45515E] block">2. Select Proficiency Level</label>
                    <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
                      {PROFICIENCY_OPTIONS.map((opt) => (
                        <button
                          key={opt.value}
                          type="button"
                          onClick={() => setNewSkillProficiency(opt.value)}
                          className={`py-2 px-2 text-xs font-bold rounded-xl border transition-all text-center ${
                            newSkillProficiency === opt.value
                              ? 'bg-[#0A0A0A] text-white border-[#0A0A0A] shadow-sm'
                              : 'bg-white text-[#45515E] border-[#E5E7EB] hover:border-[#D1D5DB]'
                          }`}
                        >
                          {opt.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex justify-end gap-2 pt-3 border-t border-[#E5E7EB]">
                    <Button size="sm" variant="ghost" onClick={() => setShowAddSkillModal(false)}>
                      Cancel
                    </Button>
                    <Button size="sm" variant="primary" icon={Check} onClick={handleAddSkill}>
                      Save Skill
                    </Button>
                  </div>
                </div>
              )}

              {/* Edit Skill Level Modal */}
              {editingSkill && (
                <div className="p-4 rounded-2xl bg-[#FFFBEB] border border-[#FDE68A] space-y-3 animate-fadeIn">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xs font-bold text-[#92400E] flex items-center gap-1.5">
                      <Sliders className="w-4 h-4" />
                      Edit Proficiency for <strong className="text-[#0A0A0A]">{editingSkill.name}</strong>
                    </h4>
                    <button onClick={() => setEditingSkill(null)} className="text-[#92400E] hover:text-[#0A0A0A]">
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
                    {PROFICIENCY_OPTIONS.map((opt) => (
                      <button
                        key={opt.value}
                        type="button"
                        onClick={() => handleUpdateSkillProficiency(editingSkill.id, opt.value)}
                        className={`py-2 px-2 text-xs font-bold rounded-xl border transition-all text-center ${
                          editingSkill.proficiency_val === opt.value
                            ? 'bg-[#92400E] text-white border-[#92400E] shadow-sm'
                            : 'bg-white text-[#45515E] border-[#FDE68A] hover:border-[#92400E]'
                        }`}
                      >
                        {opt.label}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Structured Skill Inventory Items Display */}
              {skills.length === 0 ? (
                <div className="text-center py-6 border-2 border-dashed border-[#E5E7EB] rounded-2xl bg-[#F9FAFB]">
                  <p className="text-xs font-semibold text-[#8E8E93]">No skills currently in your inventory.</p>
                  <button
                    onClick={() => setShowAddSkillModal(true)}
                    className="text-xs font-bold text-[#0066FF] hover:underline mt-1 inline-block"
                  >
                    + Add your first skill
                  </button>
                </div>
              ) : (
                <div className="flex flex-wrap gap-2.5">
                  {skills.map((sk) => (
                    <SkillChip
                      key={sk.id || sk.name}
                      name={sk.name}
                      proficiency={sk.proficiency}
                      onClick={() => setEditingSkill({
                        id: sk.id,
                        name: sk.name,
                        proficiency_val: sk.proficiency_val || (sk.proficiency === "Expert" ? 5 : sk.proficiency === "Advanced" ? 4 : sk.proficiency === "Intermediate" ? 3 : sk.proficiency === "Basic" ? 2 : 1)
                      })}
                      onRemove={() => handleRemoveSkill(sk.id, sk.name)}
                    />
                  ))}
                </div>
              )}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
