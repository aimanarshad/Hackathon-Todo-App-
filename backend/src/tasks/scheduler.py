"""Scheduler for recurring tasks and reminders."""
import asyncio
import threading
from datetime import datetime, timedelta
from typing import Callable
from sqlmodel import Session
from backend.src.tasks.recurrence_engine import RecurrenceEngine
from backend.src.services.recurring_task_service import RecurringTaskService
from backend.src.services.task_event_service import TaskEventService
from backend.src.dapr.dapr_client import DaprClient
from backend.src.dapr.task_event_producer import TaskEventProducer


class TaskScheduler:
    """Scheduler for processing recurring tasks and reminders."""

    def __init__(
        self,
        db_session: Session,
        recurrence_engine: RecurrenceEngine,
        recurring_task_service: RecurringTaskService,
        task_event_service: TaskEventService,
        dapr_client: DaprClient,
        task_event_producer: TaskEventProducer
    ):
        self.db_session = db_session
        self.recurrence_engine = recurrence_engine
        self.recurring_task_service = recurring_task_service
        self.task_event_service = task_event_service
        self.dapr_client = dapr_client
        self.task_event_producer = task_event_producer
        self.is_running = False
        self.scheduler_thread = None

    def start_scheduler(self):
        """Start the scheduler in a background thread."""
        if self.is_running:
            return

        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()

    def stop_scheduler(self):
        """Stop the scheduler."""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()

    def _scheduler_loop(self):
        """Main scheduler loop that runs continuously."""
        while self.is_running:
            try:
                # Process recurring tasks every 5 minutes
                asyncio.run(self._process_recurring_tasks())

                # Sleep for 5 minutes before next check
                for _ in range(300):  # 300 seconds = 5 minutes
                    if not self.is_running:
                        break
                    import time
                    time.sleep(1)
            except Exception as e:
                print(f"Error in scheduler loop: {str(e)}")
                # Sleep for 1 minute before retrying
                for _ in range(60):
                    if not self.is_running:
                        break
                    import time
                    time.sleep(1)

    async def _process_recurring_tasks(self):
        """Process recurring tasks and create new instances."""
        try:
            await self.recurrence_engine.process_recurring_tasks()
        except Exception as e:
            print(f"Error processing recurring tasks: {str(e)}")

    def schedule_single_task(self, delay_seconds: int, callback: Callable):
        """Schedule a single task to run after a specified delay."""
        def delayed_execution():
            import time
            time.sleep(delay_seconds)
            callback()

        thread = threading.Thread(target=delayed_execution)
        thread.daemon = True
        thread.start()
        return thread

    def schedule_periodic_task(self, interval_seconds: int, callback: Callable):
        """Schedule a periodic task to run at regular intervals."""
        def periodic_execution():
            while self.is_running:
                try:
                    callback()
                    import time
                    time.sleep(interval_seconds)
                except Exception as e:
                    print(f"Error in periodic task: {str(e)}")
                    import time
                    time.sleep(interval_seconds)

        thread = threading.Thread(target=periodic_execution)
        thread.daemon = True
        thread.start()
        return thread

    def schedule_reminder(self, reminder_datetime: datetime, task_id: int, user_id: int):
        """Schedule a reminder for a specific task."""
        now = datetime.utcnow()
        delay_seconds = (reminder_datetime - now).total_seconds()

        if delay_seconds <= 0:
            # Reminder is in the past, trigger immediately
            self._trigger_reminder(task_id, user_id)
            return

        def trigger_callback():
            self._trigger_reminder(task_id, user_id)

        self.schedule_single_task(int(delay_seconds), trigger_callback)

    def _trigger_reminder(self, task_id: int, user_id: int):
        """Trigger a reminder for a task."""
        try:
            # Publish reminder event via Dapr
            asyncio.run(
                self.task_event_producer.publish_reminder_sent(
                    reminder_id=0,  # Placeholder ID
                    task_id=task_id,
                    sent_time=datetime.utcnow(),
                    user_id=user_id
                )
            )

            # Create a task event record
            self.task_event_service.create_task_event(
                event_type="reminder_triggered",
                task_id=task_id,
                event_data={
                    "task_id": task_id,
                    "user_id": user_id,
                    "triggered_at": datetime.utcnow().isoformat()
                }
            )
        except Exception as e:
            print(f"Error triggering reminder for task {task_id}: {str(e)}")

    def schedule_recurring_task_processing(self):
        """Schedule the recurring task processing to run periodically."""
        def process_recurring_callback():
            asyncio.run(self._process_recurring_tasks())

        # Run every 5 minutes
        return self.schedule_periodic_task(300, process_recurring_callback)


# Global scheduler instance
_scheduler_instance = None


def get_scheduler() -> TaskScheduler:
    """Get the global scheduler instance."""
    return _scheduler_instance


def initialize_scheduler(
    db_session: Session,
    recurrence_engine: RecurrenceEngine,
    recurring_task_service: RecurringTaskService,
    task_event_service: TaskEventService,
    dapr_client: DaprClient,
    task_event_producer: TaskEventProducer
):
    """Initialize the global scheduler instance."""
    global _scheduler_instance
    _scheduler_instance = TaskScheduler(
        db_session=db_session,
        recurrence_engine=recurrence_engine,
        recurring_task_service=recurring_task_service,
        task_event_service=task_event_service,
        dapr_client=dapr_client,
        task_event_producer=task_event_producer
    )
    return _scheduler_instance