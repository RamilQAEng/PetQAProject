from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_kafka_producer
from ..models import Task as TaskModel
from ..schemas import TaskCreate, Task
from ..models import Task as TaskModel
from confluent_kafka import Producer

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=Task)
def create_task(
    task: TaskCreate, 
    db: Session = Depends(get_db),
    producer: Producer = Depends(get_kafka_producer)
):
    db_task = TaskModel(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Отправка сообщения в Kafka с обработкой ошибок
    try:
        producer.produce(
            'tasks', 
            key=str(db_task.id),
            value=Task.from_orm(db_task).json().encode('utf-8')
        )
        producer.flush()
    except Exception as e:
        print(f"Kafka error: {str(e)}")
    
    return db_task

@router.get("/", response_model=list[Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
