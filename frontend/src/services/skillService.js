import api from './api';

export const skillService = {
  async getAvailableSkills() {
    const res = await api.get('/skills');
    return res.data;
  },

  async getUserSkills() {
    const res = await api.get('/user-skills');
    return res.data;
  },

  async addUserSkill(skillId, proficiency, skillName = null) {
    const payload = { proficiency };
    if (skillId) payload.skill_id = skillId;
    if (skillName) payload.skill_name = skillName;
    const res = await api.post('/user-skills', payload);
    return res.data;
  },

  async updateUserSkill(userSkillId, proficiency) {
    const res = await api.put(`/user-skills/${userSkillId}`, { proficiency });
    return res.data;
  },

  async deleteUserSkill(userSkillId) {
    const res = await api.delete(`/user-skills/${userSkillId}`);
    return res.data;
  },

  async updateUserSkills(userSkills) {
    const savedResults = [];
    if (Array.isArray(userSkills)) {
      for (const item of userSkills) {
        let skillId = item.skill_id || (typeof item.id === 'number' ? item.id : null);
        let skillName = item.name || item.skill_name;
        const profMap = { "Beginner": 1, "Basic": 2, "Intermediate": 3, "Advanced": 4, "Expert": 5 };
        let profVal = item.proficiency;
        if (typeof profVal === 'string') {
          profVal = profMap[profVal] || 3;
        }
        if (!profVal || typeof profVal !== 'number') {
          profVal = 3;
        }

        try {
          const added = await this.addUserSkill(skillId, profVal, skillName);
          savedResults.push(added);
        } catch (e) {
          // ignore duplicate
        }
      }
    }
    return { success: true, userSkills: savedResults };
  }
};
