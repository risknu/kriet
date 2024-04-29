from __future__ import annotations

import re, os, sys
try:
    from mcstatus import JavaServer
    from mcstatus.status_response import JavaStatusResponse
    from mcstatus.querier import QueryResponse
except Exception as e:
    sys.exit(1)
from typing import Optional, Union, Any
from dataclasses import dataclass
from abc import ABC


@dataclass
class server_cls(object):
    players_count: Optional[int]
    latency: Optional[Union[int | float]]
    ping: Optional[Union[int | float]]
    players_names: list[Optional[str]]
    max_players: Optional[int]
    version: Optional[str]
    
def server_request(ip_addres: Optional[str] = None, port: Optional[Union[int | str]] = None) -> Optional[server_cls]:
    if ip_addres is None or port is None:
        return None
    server_object: JavaServer = JavaServer.lookup(f"{ip_addres}:{port}")
    ret_server_cls: server_cls = server_cls(None, None, None, None, None, None)
    
    status_object: JavaStatusResponse = server_object.status()
    ret_server_cls.latency = status_object.latency
    ret_server_cls.players_count = status_object.players.online
    
    ret_server_cls.ping = server_object.ping()
    
    query_object: QueryResponse = server_object.query()
    ret_server_cls.players_names= query_object.players.names
    ret_server_cls.max_players = query_object.players.max
    ret_server_cls.version = query_object.software.version
    
    return ret_server_cls
