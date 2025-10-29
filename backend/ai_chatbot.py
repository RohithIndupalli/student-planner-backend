from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator
from backend.config import settings
from backend.database import get_database
from datetime import datetime

# Define the state for our graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage | SystemMessage], operator.add]
    user_id: str
    user_context: dict

class AcademicPlannerChatbot:
    def __init__(self):
        self.llm = None
        self.graph = None
    
    def _initialize(self):
        """Lazy initialization of LLM and graph"""
        if self.llm is None:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY
            )
            self.graph = self._create_graph()
    
    async def get_user_context(self, user_id: str) -> dict:
        """Fetch user's courses, assignments, and schedules for context"""
        try:
            db = await get_database()
            
            # Get courses
            courses = await db.courses.find({"user_id": user_id}).to_list(length=None)
            
            # Get assignments
            assignments = await db.assignments.find({
                "user_id": user_id,
                "completed": False
            }).sort("due_date", 1).to_list(length=None)
            
            # Get upcoming schedules
            now = datetime.utcnow()
            schedules = await db.schedules.find({
                "user_id": user_id,
                "start_time": {"$gte": now}
            }).sort("start_time", 1).limit(10).to_list(length=None)
            
            # Format context
            context = {
                "courses": [
                    {
                        "name": c.get("course_name"),
                        "code": c.get("course_code"),
                        "instructor": c.get("instructor")
                    } for c in courses
                ],
                "assignments": [
                    {
                        "title": a.get("title"),
                        "course_id": str(a.get("course_id")),
                        "due_date": a.get("due_date").strftime("%Y-%m-%d %H:%M") if a.get("due_date") else None,
                        "priority": a.get("priority")
                    } for a in assignments[:10]  # Limit to 10 most recent
                ],
                "schedules": [
                    {
                        "title": s.get("title"),
                        "start_time": s.get("start_time").strftime("%Y-%m-%d %H:%M") if s.get("start_time") else None,
                        "end_time": s.get("end_time").strftime("%Y-%m-%d %H:%M") if s.get("end_time") else None,
                        "location": s.get("location")
                    } for s in schedules
                ]
            }
            
            return context
        except Exception as e:
            print(f"Error getting user context: {str(e)}")
            return {"courses": [], "assignments": [], "schedules": []}
    
    def _create_system_prompt(self, user_context: dict) -> str:
        """Create a system prompt with user context"""
        courses_text = "\n".join([f"- {c['name']} ({c['code']})" for c in user_context.get("courses", [])])
        assignments_text = "\n".join([
            f"- {a['title']} (Due: {a['due_date']}, Priority: {a['priority']})" 
            for a in user_context.get("assignments", [])
        ])
        schedules_text = "\n".join([
            f"- {s['title']} ({s['start_time']} to {s['end_time']})" 
            for s in user_context.get("schedules", [])
        ])
        
        return f"""You are an AI academic planning assistant for students. Your role is to help students:
1. Manage their time effectively
2. Prioritize assignments and coursework
3. Plan study schedules
4. Provide academic advice and study strategies
5. Suggest ways to balance course loads
6. Offer tips for meeting deadlines
7. Help analyze their workload and commitments

Current Student Context:

ENROLLED COURSES:
{courses_text if courses_text else "No courses enrolled yet"}

PENDING ASSIGNMENTS:
{assignments_text if assignments_text else "No pending assignments"}

UPCOMING SCHEDULE:
{schedules_text if schedules_text else "No upcoming scheduled events"}

Provide helpful, actionable advice based on the student's current academic situation. Be encouraging, practical, and specific. When suggesting study plans or time management strategies, consider their actual course load and deadlines.

If asked about specific assignments or courses, refer to the information provided above. If you don't have enough information, ask clarifying questions."""

    async def process_node(self, state: AgentState) -> AgentState:
        """Process the user's message and generate a response"""
        try:
            # Create system prompt with context
            system_prompt = self._create_system_prompt(state["user_context"])
            
            # Create messages list
            messages = [SystemMessage(content=system_prompt)] + list(state["messages"])
            
            # Get response from LLM
            response = await self.llm.ainvoke(messages)
            
            # Add AI response to messages
            return {
                "messages": [AIMessage(content=response.content)],
                "user_id": state["user_id"],
                "user_context": state["user_context"]
            }
        except Exception as e:
            error_message = f"I apologize, but I encountered an error: {str(e)}. Please try again."
            return {
                "messages": [AIMessage(content=error_message)],
                "user_id": state["user_id"],
                "user_context": state["user_context"]
            }
    
    def _create_graph(self):
        """Create the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("process", self.process_node)
        
        # Set entry point
        workflow.set_entry_point("process")
        
        # Add edge to end
        workflow.add_edge("process", END)
        
        # Compile the graph
        return workflow.compile()
    
    async def chat(self, user_id: str, message: str) -> str:
        """Main chat interface"""
        try:
            # Initialize LLM if not already done
            self._initialize()
            
            # Get user context
            user_context = await self.get_user_context(user_id)
            
            # Create initial state
            initial_state = {
                "messages": [HumanMessage(content=message)],
                "user_id": user_id,
                "user_context": user_context
            }
            
            # Run the graph
            result = await self.graph.ainvoke(initial_state)
            
            # Extract the last AI message
            ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
            if ai_messages:
                return ai_messages[-1].content
            else:
                return "I'm sorry, I couldn't generate a response. Please try again."
                
        except Exception as e:
            print(f"Chat error: {str(e)}")
            return f"I apologize, but I encountered an error processing your request. Please ensure your OpenAI API key is configured correctly and try again."

# Create a singleton instance
chatbot = AcademicPlannerChatbot()
