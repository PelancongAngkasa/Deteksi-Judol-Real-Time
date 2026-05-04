"""
Pydantic models untuk API schemas
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class WebsiteBase(BaseModel):
    url: str
    page_title: Optional[str] = None


class WebsiteCreate(WebsiteBase):
    pass


class WebsiteCreateRequest(WebsiteBase):
    """Request body untuk membuat target URL baru."""
    status: str = "active"  # active, inactive, removed


class WebsiteUpdateRequest(BaseModel):
    """Request body untuk update target URL yang sudah ada."""
    url: Optional[str] = None
    page_title: Optional[str] = None
    status: Optional[str] = None  # active, inactive, removed


class WebsiteResponse(WebsiteBase):
    id: int
    status: str
    last_scan_time: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DetectionBase(BaseModel):
    keywords_found: List[str]
    suspect_urls: List[str]
    page_title: Optional[str] = None
    severity: str = "medium"


class DetectionResponse(DetectionBase):
    id: int
    scan_id: int
    website_id: int
    website_url: Optional[str] = None  # URL dari tabel websites
    created_at: datetime

    class Config:
        from_attributes = True


class ScanBase(BaseModel):
    detected: bool
    keywords_count: int
    suspect_urls_count: int
    status_code: Optional[int] = None
    error: Optional[str] = None
    scan_duration: float = 0


class ScanCreate(ScanBase):
    website_id: int


class ScanResponse(ScanBase):
    id: int
    website_id: int
    scan_time: datetime
    detections: List[DetectionResponse] = []

    class Config:
        from_attributes = True


class HourlyStatisticResponse(BaseModel):
    hour: datetime
    total_websites_scanned: int
    total_detected: int
    detection_rate: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DashboardStatistics(BaseModel):
    total_websites: int
    total_detected_today: int
    total_detected_this_hour: int
    detection_rate: float
    last_scan_time: Optional[datetime] = None
    auto_scan_enabled: bool
    next_scan_time: Optional[datetime] = None
    hourly_data: List[HourlyStatisticResponse]
    recent_detections: List[DetectionResponse]


class DashboardResponse(BaseModel):
    status: str  # "success" atau "error"
    data: DashboardStatistics
    message: Optional[str] = None


class ScanStatusResponse(BaseModel):
    is_scanning: bool
    auto_scan_enabled: bool
    scan_interval_minutes: int
    last_scan_time: Optional[datetime] = None
    next_scan_time: Optional[datetime] = None
    total_websites: int
    total_detected_today: int


class ManualScanRequest(BaseModel):
    urls: List[str]
    priority: str = "normal"  # normal atau urgent


class ManualScanResponse(BaseModel):
    scan_id: Optional[int] = None
    status: str
    message: str
    results_count: int = 0
