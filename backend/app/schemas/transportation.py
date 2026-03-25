"""Transportation schemas."""
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TransportationBase(BaseModel):
    name: str
    category: str
    rating: Optional[float] = None
    
    route_palembang: bool = False
    route_bengkulu: bool = False
    route_lampung: bool = False
    route_jabodetabek: bool = False
    route_jawa: bool = False
    
    phone: Optional[str] = None
    maps_link: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    dist_gunung_dempo: Optional[float] = None
    dist_pasar_dempo_permai: Optional[float] = None
    dist_bandara_atung_bungsu: Optional[float] = None
    dist_rsud_besemah: Optional[float] = None
    dist_spbu_air_perikan: Optional[float] = None
    dist_spbu_simpang_manna: Optional[float] = None
    dist_spbu_pengandonan: Optional[float] = None
    dist_spbu_karang_dalo: Optional[float] = None
    
    is_active: bool = True

class TransportationCreate(TransportationBase):
    pass

class TransportationUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    
    route_palembang: Optional[bool] = None
    route_bengkulu: Optional[bool] = None
    route_lampung: Optional[bool] = None
    route_jabodetabek: Optional[bool] = None
    route_jawa: Optional[bool] = None
    
    phone: Optional[str] = None
    maps_link: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    dist_gunung_dempo: Optional[float] = None
    dist_pasar_dempo_permai: Optional[float] = None
    dist_bandara_atung_bungsu: Optional[float] = None
    dist_rsud_besemah: Optional[float] = None
    dist_spbu_air_perikan: Optional[float] = None
    dist_spbu_simpang_manna: Optional[float] = None
    dist_spbu_pengandonan: Optional[float] = None
    dist_spbu_karang_dalo: Optional[float] = None
    
    is_active: Optional[bool] = None

class TransportationResponse(TransportationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
