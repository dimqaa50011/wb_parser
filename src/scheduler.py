from pytz import timezone
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor


jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///data/jobs.sqlite")}
executors = {"default": AsyncIOExecutor()}
job_defaults = {"coalesce": False, "max_instances": 3}

scheduler = AsyncIOScheduler(jobstores=jobstores, job_defaults=job_defaults)
