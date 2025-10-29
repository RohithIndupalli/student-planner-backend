import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { assignmentsAPI, coursesAPI, schedulesAPI } from '../services/api';
import toast from 'react-hot-toast';
import {
  BookOpen,
  ClipboardList,
  Calendar,
  AlertCircle,
  CheckCircle,
  Clock,
  TrendingUp,
} from 'lucide-react';
import { format, isToday, isTomorrow, isPast, differenceInDays } from 'date-fns';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalCourses: 0,
    totalAssignments: 0,
    pendingAssignments: 0,
    upcomingSchedules: 0,
  });
  const [recentAssignments, setRecentAssignments] = useState([]);
  const [upcomingSchedules, setUpcomingSchedules] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [coursesRes, assignmentsRes, schedulesRes] = await Promise.all([
        coursesAPI.getAll(),
        assignmentsAPI.getAll(),
        schedulesAPI.getAll(),
      ]);

      const courses = coursesRes.data;
      const assignments = assignmentsRes.data;
      const schedules = schedulesRes.data;

      const pendingAssignments = assignments.filter((a) => !a.completed);
      const now = new Date();
      const upcoming = schedules.filter((s) => new Date(s.start_time) > now);

      setStats({
        totalCourses: courses.length,
        totalAssignments: assignments.length,
        pendingAssignments: pendingAssignments.length,
        upcomingSchedules: upcoming.length,
      });

      setRecentAssignments(pendingAssignments.slice(0, 5));
      setUpcomingSchedules(upcoming.slice(0, 5));
      setLoading(false);
    } catch (error) {
      toast.error('Failed to load dashboard data');
      setLoading(false);
    }
  };

  const getAssignmentPriority = (assignment) => {
    const dueDate = new Date(assignment.due_date);
    const daysUntilDue = differenceInDays(dueDate, new Date());

    if (isPast(dueDate)) {
      return { color: 'bg-red-100 text-red-800', label: 'Overdue', icon: AlertCircle };
    } else if (daysUntilDue <= 1) {
      return { color: 'bg-orange-100 text-orange-800', label: 'Due Soon', icon: Clock };
    } else if (assignment.priority === 'high') {
      return { color: 'bg-yellow-100 text-yellow-800', label: 'High Priority', icon: TrendingUp };
    } else {
      return { color: 'bg-green-100 text-green-800', label: 'On Track', icon: CheckCircle };
    }
  };

  const formatScheduleTime = (schedule) => {
    const start = new Date(schedule.start_time);
    if (isToday(start)) {
      return `Today at ${format(start, 'h:mm a')}`;
    } else if (isTomorrow(start)) {
      return `Tomorrow at ${format(start, 'h:mm a')}`;
    } else {
      return format(start, 'MMM d, h:mm a');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  const statCards = [
    {
      title: 'Total Courses',
      value: stats.totalCourses,
      icon: BookOpen,
      color: 'bg-blue-500',
      onClick: () => navigate('/courses'),
    },
    {
      title: 'Pending Assignments',
      value: stats.pendingAssignments,
      icon: ClipboardList,
      color: 'bg-purple-500',
      onClick: () => navigate('/assignments'),
    },
    {
      title: 'Total Assignments',
      value: stats.totalAssignments,
      icon: CheckCircle,
      color: 'bg-green-500',
      onClick: () => navigate('/assignments'),
    },
    {
      title: 'Upcoming Events',
      value: stats.upcomingSchedules,
      icon: Calendar,
      color: 'bg-orange-500',
      onClick: () => navigate('/schedule'),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">Welcome to Your Dashboard</h1>
        <p className="text-indigo-100">
          Here's an overview of your academic activities and upcoming tasks
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div
              key={index}
              onClick={stat.onClick}
              className="card cursor-pointer hover:scale-105 transition-transform"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Assignments */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900">Pending Assignments</h2>
            <button
              onClick={() => navigate('/assignments')}
              className="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
            >
              View All
            </button>
          </div>
          <div className="space-y-3">
            {recentAssignments.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No pending assignments</p>
            ) : (
              recentAssignments.map((assignment) => {
                const priority = getAssignmentPriority(assignment);
                const PriorityIcon = priority.icon;
                return (
                  <div
                    key={assignment.id}
                    className="p-4 border border-gray-200 rounded-lg hover:border-indigo-300 transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">{assignment.title}</h3>
                        <p className="text-sm text-gray-600 mt-1">{assignment.course_name}</p>
                        <p className="text-xs text-gray-500 mt-1">
                          Due: {format(new Date(assignment.due_date), 'MMM d, yyyy h:mm a')}
                        </p>
                      </div>
                      <span
                        className={`${priority.color} px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1`}
                      >
                        <PriorityIcon className="w-3 h-3" />
                        {priority.label}
                      </span>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Upcoming Schedule */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900">Upcoming Schedule</h2>
            <button
              onClick={() => navigate('/schedule')}
              className="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
            >
              View All
            </button>
          </div>
          <div className="space-y-3">
            {upcomingSchedules.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No upcoming events</p>
            ) : (
              upcomingSchedules.map((schedule) => (
                <div
                  key={schedule.id}
                  className="p-4 border border-gray-200 rounded-lg hover:border-indigo-300 transition-colors"
                >
                  <div className="flex items-start gap-3">
                    <div className="bg-indigo-100 p-2 rounded-lg">
                      <Calendar className="w-5 h-5 text-indigo-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">{schedule.title}</h3>
                      {schedule.course_name && (
                        <p className="text-sm text-gray-600 mt-1">{schedule.course_name}</p>
                      )}
                      <p className="text-xs text-gray-500 mt-1">
                        {formatScheduleTime(schedule)}
                      </p>
                      {schedule.location && (
                        <p className="text-xs text-gray-500">📍 {schedule.location}</p>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            onClick={() => navigate('/courses')}
            className="btn-primary py-3 flex items-center justify-center gap-2"
          >
            <BookOpen className="w-5 h-5" />
            Add Course
          </button>
          <button
            onClick={() => navigate('/assignments')}
            className="btn-primary py-3 flex items-center justify-center gap-2"
          >
            <ClipboardList className="w-5 h-5" />
            Add Assignment
          </button>
          <button
            onClick={() => navigate('/chat')}
            className="btn-primary py-3 flex items-center justify-center gap-2"
          >
            <TrendingUp className="w-5 h-5" />
            Get AI Advice
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
