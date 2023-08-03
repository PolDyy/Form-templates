from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class FederalProjectsDelayed:
    id: Optional[int] = None
    federal_prj_id: Optional[int] = None
    federal_org_id: Optional[int] = None
    prj_date: Optional[datetime] = None
    year_no: Optional[int] = None
    year_plan: Optional[int] = None
    year_achieved_cnt: Optional[int] = None
    year_achieved_percent: Optional[float] = None
    year_left_cnt: Optional[int] = None
    year_left_percent: Optional[float] = None
    year_delayed_cnt: Optional[int] = None
    year_delayed_percent: Optional[float] = None
    total_delayed_cnt: Optional[int] = None
    total_delayed_percent: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
    relevance_dttm: Optional[datetime] = None

    def as_string(self):
        string = f"""
id:                         {self.id}         
federal_prj_id:             {self.federal_prj_id}          
federal_org_id:             {self.federal_org_id}        
prj_date:                   {self.prj_date}    
year_no:                    {self.year_no}    
year_plan:                  {self.year_plan}
year_achieved_cnt:          {self.year_achieved_cnt}
year_achieved_percent:      {self.year_achieved_percent}        
year_left_cnt:              {self.year_left_cnt}
year_left_percent:          {self.year_left_percent}    
year_delayed_cnt:           {self.year_delayed_cnt}  
year_delayed_percent:       {self.year_delayed_percent}    
total_delayed_cnt:          {self.total_delayed_cnt}    
total_delayed_percent:      {self.total_delayed_percent}        
created_at:                 {self.created_at}    
updated_at:                 {self.updated_at}    
created_from:               {self.created_from}        
created_to:                 {self.created_to}        
relevance_dttm:             {self.relevance_dttm}        
        """
        return string


@dataclass
class FederalProjects:
    id: Optional[int] = None
    name: Optional[str] = None

    def as_string(self):
        return f"""
id          {self.id}
name        {self.name}
        """


@dataclass
class FederalOrganizations:
    id: Optional[int] = None
    name: Optional[str] = None

    def as_string(self):
        return f"""
id          {self.id}
name        {self.name}
        """


@dataclass
class CommonFederalProjectsDelayed:
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
    relevance_dttm: Optional[datetime] = None
