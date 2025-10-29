import React, { useState, useEffect } from 'react';
import { schedulesAPI, coursesAPI } from '../services/api';
import toast from 'react-hot-toast';
import { Plus, Edit2, Trash2, Calendar, X, MapPin, Clock } from 'lucide-react';
import { format } from 'date-fns';

const Schedule = () => {
  const [schedules, setSchedules] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingSchedule, setEditingSchedule] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    course_id: '',
    start_time: '',
    end_time: '',
    day_of_week: '',
    location: '',
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [schedulesRes, coursesRes] = await Promise.all([
        schedulesAPI.getAll(),
        coursesAPI.getAll(),
      ]);
      setSchedules(schedulesRes.data);
      setCourses(coursesRes.data);
      setLoading(false);
    } catch (error) {
      toast.error('Failed to load data');
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = {
        ...formData,
        course_id: formData.course_id || null,
      };

      if (editingSchedule) {
        await schedulesAPI.update(editingSchedule.id, submitData);
        toast.success('Schedule updated successfully');
      } else {
        await schedulesAPI.create(submitData);
        toast.success('Schedule created successfully! Email notification sent.');
      }
      fetchData();
      closeModal();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to save schedule');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this schedule?')) {
      try {
        await schedulesAPI.delete(id);
        toast.success('Schedule deleted successfully');
        fetchData();
      } catch (error) {
        toast.error('Failed to delete schedule');
      }
    }
  };

  const openModal = (schedule = null) => {
    if (schedule) {
      setEditingSchedule(schedule);
      setFormData({
        title: schedule.title,
        description: schedule.description || '',
        course_id: schedule.course_id || '',
        start_time: format(new Date(schedule.start_time), "yyyy-MM-dd'T'HH:mm"),
        end_time: format(new Date(schedule.end_time), "yyyy-MM-dd'T'HH:mm"),
        day_of_week: schedule.day_of_week || '',
        location: schedule.location || '',
      });
    } else {
      setEditingSchedule(null);
      setFormData({
        title: '',
        description: '',
        course_id: '',
        start_time: '',
        end_time: '',
        day_of_week: '',
        location: '',
      });
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingSchedule(null);
  };

  const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Schedule</h1>
        <button onClick={() => openModal()} className="btn-primary flex items-center gap-2">
          <Plus className="w-5 h-5" />
          Add Schedule
        </button>
      </div>

      {schedules.length === 0 ? (
        <div className="card text-center py-12">
          <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No schedules yet</h3>
          <p className="text-gray-600 mb-4">Get started by adding your first schedule</p>
          <button onClick={() => openModal()} className="btn-primary">
            Add Your First Schedule
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {schedules.map((schedule) => (
            <div key={schedule.id} className="card">
              <div className="flex items-start gap-4">
                <div className="bg-indigo-100 p-3 rounded-lg flex-shrink-0">
                  <Calendar className="w-6 h-6 text-indigo-600" />
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-gray-900">{schedule.title}</h3>
                      {schedule.course_name && (
                        <p className="text-sm text-indigo-600 mt-1">{schedule.course_name}</p>
                      )}
                      {schedule.description && (
                        <p className="text-sm text-gray-500 mt-2">{schedule.description}</p>
                      )}
                      <div className="flex flex-wrap items-center gap-4 mt-3">
                        <div className="flex items-center gap-1 text-sm text-gray-600">
                          <Clock className="w-4 h-4" />
                          {format(new Date(schedule.start_time), 'MMM d, yyyy h:mm a')} -{' '}
                          {format(new Date(schedule.end_time), 'h:mm a')}
                        </div>
                        {schedule.day_of_week && (
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                            {schedule.day_of_week}
                          </span>
                        )}
                        {schedule.location && (
                          <div className="flex items-center gap-1 text-sm text-gray-600">
                            <MapPin className="w-4 h-4" />
                            {schedule.location}
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="flex gap-2 flex-shrink-0">
                      <button
                        onClick={() => openModal(schedule)}
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(schedule.id)}
                        className="text-gray-600 hover:text-red-600"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900">
                {editingSchedule ? 'Edit Schedule' : 'Add New Schedule'}
              </h2>
              <button onClick={closeModal} className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Event Title *
                </label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="input-field"
                  placeholder="e.g., Math Lecture"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Course (Optional)
                </label>
                <select
                  value={formData.course_id}
                  onChange={(e) => setFormData({ ...formData, course_id: e.target.value })}
                  className="input-field"
                >
                  <option value="">No course</option>
                  {courses.map((course) => (
                    <option key={course.id} value={course.id}>
                      {course.course_name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Start Time *
                </label>
                <input
                  type="datetime-local"
                  required
                  value={formData.start_time}
                  onChange={(e) => setFormData({ ...formData, start_time: e.target.value })}
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  End Time *
                </label>
                <input
                  type="datetime-local"
                  required
                  value={formData.end_time}
                  onChange={(e) => setFormData({ ...formData, end_time: e.target.value })}
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Day of Week (Optional)
                </label>
                <select
                  value={formData.day_of_week}
                  onChange={(e) => setFormData({ ...formData, day_of_week: e.target.value })}
                  className="input-field"
                >
                  <option value="">Select day</option>
                  {daysOfWeek.map((day) => (
                    <option key={day} value={day}>
                      {day}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Location (Optional)
                </label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="input-field"
                  placeholder="e.g., Room 101, Building A"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description (Optional)
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="input-field"
                  rows="3"
                  placeholder="Event details..."
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button type="submit" className="btn-primary flex-1">
                  {editingSchedule ? 'Update Schedule' : 'Add Schedule'}
                </button>
                <button type="button" onClick={closeModal} className="btn-secondary flex-1">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Schedule;
