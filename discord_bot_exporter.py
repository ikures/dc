#!/usr/bin/env python3

import argparse
import asyncio
import datetime
import json
import os
import sys
import time
import random
import string
import uuid
import re
import hashlib
import base64
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple, Union, Set

import aiohttp
import colorama
from colorama import Fore, Style, Back

# Initialize colorama
colorama.init(autoreset=True)

# Discord logo and symbols
DISCORD_LOGO = f"""
{Fore.BLUE}          ██████{Fore.LIGHTBLUE_EX}╗ {Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╗{Fore.MAGENTA}███████{Fore.LIGHTMAGENTA_EX}╗{Fore.MAGENTA}██████{Fore.LIGHTMAGENTA_EX}╗{Fore.MAGENTA}██████{Fore.LIGHTMAGENTA_EX}╗{Fore.MAGENTA} ██████{Fore.LIGHTMAGENTA_EX}╗{Fore.MAGENTA}██████{Fore.LIGHTMAGENTA_EX}╗{Fore.MAGENTA} ██████{Fore.LIGHTMAGENTA_EX}╗ 
{Fore.BLUE}          ██{Fore.LIGHTBLUE_EX}╔══{Fore.BLUE}██{Fore.LIGHTBLUE_EX}╗{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╔════╝{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╔════╝{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╔═══{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╗{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╔══{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╗{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╔══{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╗{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╔══{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╗
{Fore.BLUE}          ██{Fore.LIGHTBLUE_EX}║  {Fore.BLUE}██{Fore.LIGHTBLUE_EX}║{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║{Fore.MAGENTA}███████{Fore.LIGHTMAGENTA_EX}╗{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║     {Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║   {Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║{Fore.MAGENTA}██████{Fore.LIGHTMAGENTA_EX}╔╝{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║  {Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║  {Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║
{Fore.BLUE}          ██{Fore.LIGHTBLUE_EX}║  {Fore.BLUE}██{Fore.LIGHTBLUE_EX}║{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║╚════{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║     {Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║   {Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╔══{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}╗{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║  {Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║  {Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║
{Fore.BLUE}          ██████{Fore.LIGHTBLUE_EX}╔╝{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║{Fore.MAGENTA}███████{Fore.LIGHTMAGENTA_EX}║╚{Fore.MAGENTA}██████{Fore.LIGHTMAGENTA_EX}╗╚{Fore.MAGENTA}██████{Fore.LIGHTMAGENTA_EX}╔╝{Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║  {Fore.MAGENTA}██{Fore.LIGHTMAGENTA_EX}║{Fore.MAGENTA}██████{Fore.LIGHTMAGENTA_EX}╔╝{Fore.MAGENTA}██████{Fore.LIGHTMAGENTA_EX}╔╝
{Fore.BLUE}          ╚═════╝ {Fore.LIGHTMAGENTA_EX}╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═════╝ 
{Fore.CYAN}                 Bot Data Exporter & Utility Tool
{Style.RESET_ALL}"""

DISCORD_SYMBOLS = [
    f"{Fore.BLUE}⚡{Style.RESET_ALL}",
    f"{Fore.MAGENTA}🎮{Style.RESET_ALL}",
    f"{Fore.LIGHTBLUE_EX}🔊{Style.RESET_ALL}",
    f"{Fore.LIGHTMAGENTA_EX}🎭{Style.RESET_ALL}",
    f"{Fore.BLUE}🎯{Style.RESET_ALL}",
    f"{Fore.MAGENTA}🏆{Style.RESET_ALL}",
    f"{Fore.LIGHTBLUE_EX}🎪{Style.RESET_ALL}",
    f"{Fore.LIGHTMAGENTA_EX}🎲{Style.RESET_ALL}"
]

def get_random_symbol():
    return random.choice(DISCORD_SYMBOLS)

# Initialize colorama
colorama.init(autoreset=True)

# Constants
API_ENDPOINT = "https://discord.com/api/v10"
USER_AGENT = "DiscordBotExporter/1.0"
RATE_LIMIT_RETRY_DELAY = 5  # seconds
DEFAULT_PREFIX = "!"
MESSAGE_TYPES = {
    0: "DEFAULT",
    1: "RECIPIENT_ADD",
    2: "RECIPIENT_REMOVE",
    3: "CALL",
    4: "CHANNEL_NAME_CHANGE",
    5: "CHANNEL_ICON_CHANGE",
    6: "CHANNEL_PINNED_MESSAGE",
    7: "GUILD_MEMBER_JOIN",
    8: "USER_PREMIUM_GUILD_SUBSCRIPTION",
    9: "USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1",
    10: "USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2",
    11: "USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3",
    12: "CHANNEL_FOLLOW_ADD",
    14: "GUILD_DISCOVERY_DISQUALIFIED",
    15: "GUILD_DISCOVERY_REQUALIFIED",
    16: "GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING",
    17: "GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING",
    18: "THREAD_CREATED",
    19: "REPLY",
    20: "CHAT_INPUT_COMMAND",
    21: "THREAD_STARTER_MESSAGE",
    22: "GUILD_INVITE_REMINDER",
    23: "CONTEXT_MENU_COMMAND",
    24: "AUTO_MODERATION_ACTION",
    25: "ROLE_SUBSCRIPTION_PURCHASE",
    26: "INTERACTION_PREMIUM_UPSELL",
    27: "STAGE_START",
    28: "STAGE_END",
    29: "STAGE_SPEAKER",
    30: "STAGE_RAISE_HAND",
    31: "STAGE_TOPIC",
    32: "GUILD_APPLICATION_PREMIUM_SUBSCRIPTION"
}

class DiscordExporter:
    def __init__(self):
        self.token = None
        self.bot_id = None
        self.headers = {}
        self.session = None
        self.is_token_auth = False
        self.export_data = {}
        
        print(f"{Fore.LIGHTBLUE_EX}🤖 Discord Bot Exporter initialized{Style.RESET_ALL}")

    async def initialize_session(self):
        """Initialize aiohttp session"""
        self.session = aiohttp.ClientSession()
        
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()

    def set_token(self, token: str):
        """Set bot token and prepare headers"""
        self.token = token
        self.is_token_auth = True
        self.headers = {
            "Authorization": f"Bot {token}",
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json"
        }
        
        # Try to extract bot ID from token
        try:
            # Bot tokens are structured as: <bot_id>.<random_string>
            parts = token.split('.')
            if len(parts) >= 2:
                self.bot_id = parts[0]
        except Exception:
            pass

    def set_bot_id(self, bot_id: str):
        """Set bot ID"""
        self.bot_id = bot_id
        self.is_token_auth = False
        # No auth headers for bot ID lookup since we're using public APIs

    async def make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
        """Make a request to the Discord API with rate limit handling"""
        if not self.session:
            await self.initialize_session()
            
        url = f"{API_ENDPOINT}{endpoint}"
        
        retry_attempts = 3
        while retry_attempts > 0:
            try:
                if method == "GET":
                    response = await self.session.get(url, headers=self.headers)
                elif method == "POST":
                    response = await self.session.post(url, headers=self.headers, json=data)
                elif method == "PUT":
                    response = await self.session.put(url, headers=self.headers, json=data)
                elif method == "DELETE":
                    response = await self.session.delete(url, headers=self.headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Handle rate limits
                if response.status == 429:
                    retry_after = int(response.headers.get('Retry-After', RATE_LIMIT_RETRY_DELAY))
                    print(f"{Fore.YELLOW}Rate limited. Retrying in {retry_after} seconds...{Style.RESET_ALL}")
                    await asyncio.sleep(retry_after)
                    continue
                
                # Handle other status codes
                if response.status == 401:
                    print(f"{Fore.RED}Authentication failed. Please check your token.{Style.RESET_ALL}")
                    sys.exit(1)
                elif response.status == 403:
                    print(f"{Fore.RED}Forbidden. The bot doesn't have permission to access this resource.{Style.RESET_ALL}")
                    return {}
                elif response.status == 404:
                    print(f"{Fore.YELLOW}Resource not found at {url}{Style.RESET_ALL}")
                    return {}
                elif 400 <= response.status < 500:
                    print(f"{Fore.RED}Client error: {response.status} for {url}{Style.RESET_ALL}")
                    return {}
                elif 500 <= response.status < 600:
                    print(f"{Fore.RED}Server error: {response.status} for {url}{Style.RESET_ALL}")
                    retry_attempts -= 1
                    await asyncio.sleep(RATE_LIMIT_RETRY_DELAY)
                    continue
                
                # Process successful response
                if response.status == 204:  # No content
                    return {}
                
                return await response.json()
                
            except aiohttp.ClientError as e:
                print(f"{Fore.RED}Request error: {str(e)}{Style.RESET_ALL}")
                retry_attempts -= 1
                await asyncio.sleep(RATE_LIMIT_RETRY_DELAY)
            except Exception as e:
                print(f"{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
                retry_attempts -= 1
                await asyncio.sleep(RATE_LIMIT_RETRY_DELAY)
        
        print(f"{Fore.RED}Failed to complete request after multiple attempts.{Style.RESET_ALL}")
        return {}

    async def export_basic_info(self):
        """Export basic bot information"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Limited information available without token authentication.{Style.RESET_ALL}")
            # Try to get public bot info from public APIs or approximations
            return
            
        try:
            application_info = await self.make_request('/oauth2/applications/@me')
            self.export_data['application_info'] = application_info
            
            user_info = await self.make_request('/users/@me')
            self.export_data['user_info'] = user_info
            
            print(f"{Fore.GREEN}✓ Exported basic bot information{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export basic info: {str(e)}{Style.RESET_ALL}")

    async def export_guilds(self):
        """Export all guilds the bot is in"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export guilds without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guilds = await self.make_request('/users/@me/guilds')
            self.export_data['guilds'] = guilds
            
            # Get detailed information for each guild
            detailed_guilds = []
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    detailed_guild = await self.make_request(f'/guilds/{guild_id}')
                    if detailed_guild:
                        detailed_guilds.append(detailed_guild)
                        # Don't hit rate limits too hard
                        await asyncio.sleep(0.5)
            
            self.export_data['detailed_guilds'] = detailed_guilds
            print(f"{Fore.GREEN}✓ Exported {len(guilds)} guilds with detailed information{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export guilds: {str(e)}{Style.RESET_ALL}")

    async def export_commands(self):
        """Export all application commands"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export commands without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            application_id = self.export_data.get('application_info', {}).get('id')
            if not application_id and self.bot_id:
                application_id = self.bot_id
                
            if not application_id:
                print(f"{Fore.YELLOW}Cannot export commands without application ID.{Style.RESET_ALL}")
                return
                
            global_commands = await self.make_request(f'/applications/{application_id}/commands')
            self.export_data['global_commands'] = global_commands
            
            # Get guild-specific commands for each guild
            guild_commands = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    commands = await self.make_request(f'/applications/{application_id}/guilds/{guild_id}/commands')
                    if commands:
                        guild_commands[guild_id] = commands
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_commands'] = guild_commands
            print(f"{Fore.GREEN}✓ Exported {len(global_commands)} global commands and guild-specific commands for {len(guild_commands)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export commands: {str(e)}{Style.RESET_ALL}")

    async def export_permissions(self):
        """Export permission settings"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export permissions without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            application_id = self.export_data.get('application_info', {}).get('id')
            if not application_id and self.bot_id:
                application_id = self.bot_id
                
            if not application_id:
                print(f"{Fore.YELLOW}Cannot export permissions without application ID.{Style.RESET_ALL}")
                return
            
            # Get guild-specific permissions for each guild
            guild_permissions = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    permissions = await self.make_request(
                        f'/applications/{application_id}/guilds/{guild_id}/commands/permissions'
                    )
                    if permissions:
                        guild_permissions[guild_id] = permissions
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_permissions'] = guild_permissions
            print(f"{Fore.GREEN}✓ Exported permissions for {len(guild_permissions)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export permissions: {str(e)}{Style.RESET_ALL}")

    async def export_channels(self):
        """Export channels in guilds"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export channels without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_channels = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    channels = await self.make_request(f'/guilds/{guild_id}/channels')
                    if channels:
                        guild_channels[guild_id] = channels
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_channels'] = guild_channels
            
            channel_count = sum(len(channels) for channels in guild_channels.values())
            print(f"{Fore.GREEN}✓ Exported {channel_count} channels from {len(guild_channels)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export channels: {str(e)}{Style.RESET_ALL}")

    async def export_webhooks(self):
        """Export webhook information"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export webhooks without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            application_id = self.export_data.get('application_info', {}).get('id')
            if not application_id:
                print(f"{Fore.YELLOW}Cannot export webhooks without application ID.{Style.RESET_ALL}")
                return
                
            webhooks = await self.make_request(f'/applications/{application_id}/webhooks')
            self.export_data['webhooks'] = webhooks
            
            print(f"{Fore.GREEN}✓ Exported {len(webhooks)} application webhooks{Style.RESET_ALL}")
            
            # Also export guild webhooks
            guild_webhooks = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    webhooks = await self.make_request(f'/guilds/{guild_id}/webhooks')
                    if webhooks:
                        guild_webhooks[guild_id] = webhooks
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_webhooks'] = guild_webhooks
            
            webhook_count = sum(len(webhooks) for webhooks in guild_webhooks.values())
            print(f"{Fore.GREEN}✓ Exported {webhook_count} webhooks from {len(guild_webhooks)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export webhooks: {str(e)}{Style.RESET_ALL}")

    async def export_interactions(self):
        """Export recent interactions (limited)"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export interactions without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            # There's no direct API to get all interactions, so we export summary stats
            # This is a placeholder for what could be a webhook-based collector
            self.export_data['interactions'] = {
                "note": "Discord API doesn't provide historical interaction data. Set up a webhook to log interactions."
            }
            
            print(f"{Fore.YELLOW}Limited interaction data available through API.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export interactions: {str(e)}{Style.RESET_ALL}")

    async def export_presence(self):
        """Export presence configuration"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export presence without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            # Discord API doesn't have a direct endpoint to get current presence settings
            # Extract from gateway connection if possible
            user_info = self.export_data.get('user_info', {})
            self.export_data['presence'] = {
                "status": "Presence details cannot be directly exported from API",
                "bot_user": user_info
            }
            
            print(f"{Fore.YELLOW}Limited presence data available through API.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export presence: {str(e)}{Style.RESET_ALL}")

    async def export_voice_settings(self):
        """Export voice configuration and state"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export voice settings without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            voice_regions = await self.make_request('/voice/regions')
            self.export_data['voice_regions'] = voice_regions
            
            # Get voice states from guilds
            guild_voice_states = {}
            guilds = self.export_data.get('detailed_guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                voice_states = guild.get('voice_states', [])
                if guild_id and voice_states:
                    guild_voice_states[guild_id] = voice_states
            
            self.export_data['guild_voice_states'] = guild_voice_states
            
            print(f"{Fore.GREEN}✓ Exported voice regions and current voice states{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export voice settings: {str(e)}{Style.RESET_ALL}")

    async def export_emoji(self):
        """Export custom emoji information"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export emoji without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_emojis = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    emojis = await self.make_request(f'/guilds/{guild_id}/emojis')
                    if emojis:
                        guild_emojis[guild_id] = emojis
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_emojis'] = guild_emojis
            
            emoji_count = sum(len(emojis) for emojis in guild_emojis.values())
            print(f"{Fore.GREEN}✓ Exported {emoji_count} custom emoji from {len(guild_emojis)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export emoji: {str(e)}{Style.RESET_ALL}")

    async def export_stickers(self):
        """Export custom sticker information"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export stickers without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_stickers = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    stickers = await self.make_request(f'/guilds/{guild_id}/stickers')
                    if stickers:
                        guild_stickers[guild_id] = stickers
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_stickers'] = guild_stickers
            
            sticker_count = sum(len(stickers) for stickers in guild_stickers.values())
            print(f"{Fore.GREEN}✓ Exported {sticker_count} custom stickers from {len(guild_stickers)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export stickers: {str(e)}{Style.RESET_ALL}")

    async def export_scheduled_events(self):
        """Export scheduled events information"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export scheduled events without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_events = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    events = await self.make_request(f'/guilds/{guild_id}/scheduled-events')
                    if events:
                        guild_events[guild_id] = events
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_events'] = guild_events
            
            event_count = sum(len(events) for events in guild_events.values())
            print(f"{Fore.GREEN}✓ Exported {event_count} scheduled events from {len(guild_events)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export scheduled events: {str(e)}{Style.RESET_ALL}")

    async def export_roles(self):
        """Export role configuration"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export roles without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_roles = {}
            guilds = self.export_data.get('detailed_guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                roles = guild.get('roles', [])
                if guild_id and roles:
                    guild_roles[guild_id] = roles
            
            self.export_data['guild_roles'] = guild_roles
            
            role_count = sum(len(roles) for roles in guild_roles.values())
            print(f"{Fore.GREEN}✓ Exported {role_count} roles from {len(guild_roles)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export roles: {str(e)}{Style.RESET_ALL}")

    async def export_invites(self):
        """Export active invites"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export invites without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_invites = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    invites = await self.make_request(f'/guilds/{guild_id}/invites')
                    if invites:
                        guild_invites[guild_id] = invites
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_invites'] = guild_invites
            
            invite_count = sum(len(invites) for invites in guild_invites.values())
            print(f"{Fore.GREEN}✓ Exported {invite_count} active invites from {len(guild_invites)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export invites: {str(e)}{Style.RESET_ALL}")

    async def export_bans(self):
        """Export ban lists"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export bans without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_bans = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    bans = await self.make_request(f'/guilds/{guild_id}/bans')
                    if bans:
                        guild_bans[guild_id] = bans
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_bans'] = guild_bans
            
            ban_count = sum(len(bans) for bans in guild_bans.values())
            print(f"{Fore.GREEN}✓ Exported {ban_count} bans from {len(guild_bans)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export bans: {str(e)}{Style.RESET_ALL}")

    async def export_audit_logs(self):
        """Export recent audit logs (limited by API)"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export audit logs without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_audit_logs = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    audit_logs = await self.make_request(f'/guilds/{guild_id}/audit-logs?limit=100')
                    if audit_logs:
                        guild_audit_logs[guild_id] = audit_logs
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_audit_logs'] = guild_audit_logs
            
            log_count = sum(len(logs.get('audit_log_entries', [])) for logs in guild_audit_logs.values())
            print(f"{Fore.GREEN}✓ Exported {log_count} audit log entries from {len(guild_audit_logs)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export audit logs: {str(e)}{Style.RESET_ALL}")

    async def export_widget_settings(self):
        """Export widget configuration"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export widget settings without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_widgets = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    widget = await self.make_request(f'/guilds/{guild_id}/widget')
                    if widget:
                        guild_widgets[guild_id] = widget
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_widgets'] = guild_widgets
            print(f"{Fore.GREEN}✓ Exported widget settings from {len(guild_widgets)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export widget settings: {str(e)}{Style.RESET_ALL}")

    async def export_integrations(self):
        """Export integrations information"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export integrations without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_integrations = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    integrations = await self.make_request(f'/guilds/{guild_id}/integrations')
                    if integrations:
                        guild_integrations[guild_id] = integrations
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_integrations'] = guild_integrations
            
            integration_count = sum(len(integrations) for integrations in guild_integrations.values())
            print(f"{Fore.GREEN}✓ Exported {integration_count} integrations from {len(guild_integrations)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export integrations: {str(e)}{Style.RESET_ALL}")

    async def export_templates(self):
        """Export guild templates"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export templates without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_templates = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    templates = await self.make_request(f'/guilds/{guild_id}/templates')
                    if templates:
                        guild_templates[guild_id] = templates
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_templates'] = guild_templates
            
            template_count = sum(len(templates) for templates in guild_templates.values())
            print(f"{Fore.GREEN}✓ Exported {template_count} templates from {len(guild_templates)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export templates: {str(e)}{Style.RESET_ALL}")

    async def export_welcome_screens(self):
        """Export guild welcome screens"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export welcome screens without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_welcome_screens = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    welcome_screen = await self.make_request(f'/guilds/{guild_id}/welcome-screen')
                    if welcome_screen:
                        guild_welcome_screens[guild_id] = welcome_screen
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_welcome_screens'] = guild_welcome_screens
            print(f"{Fore.GREEN}✓ Exported welcome screens from {len(guild_welcome_screens)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export welcome screens: {str(e)}{Style.RESET_ALL}")

    async def export_auto_moderation(self):
        """Export auto-moderation rules"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export auto-moderation without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            guild_auto_mod_rules = {}
            guilds = self.export_data.get('guilds', [])
            for guild in guilds:
                guild_id = guild.get('id')
                if guild_id:
                    rules = await self.make_request(f'/guilds/{guild_id}/auto-moderation/rules')
                    if rules:
                        guild_auto_mod_rules[guild_id] = rules
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['guild_auto_mod_rules'] = guild_auto_mod_rules
            
            rule_count = sum(len(rules) for rules in guild_auto_mod_rules.values())
            print(f"{Fore.GREEN}✓ Exported {rule_count} auto-moderation rules from {len(guild_auto_mod_rules)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export auto-moderation rules: {str(e)}{Style.RESET_ALL}")

    async def export_stage_instances(self):
        """Export stage channel instances"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export stage instances without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            stage_instances = await self.make_request('/stage-instances')
            self.export_data['stage_instances'] = stage_instances
            
            print(f"{Fore.GREEN}✓ Exported {len(stage_instances)} active stage instances{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export stage instances: {str(e)}{Style.RESET_ALL}")

    async def export_application_role_connections(self):
        """Export role connection metadata"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export role connections without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            application_id = self.export_data.get('application_info', {}).get('id')
            if not application_id and self.bot_id:
                application_id = self.bot_id
                
            if not application_id:
                print(f"{Fore.YELLOW}Cannot export role connections without application ID.{Style.RESET_ALL}")
                return
                
            role_connections = await self.make_request(f'/applications/{application_id}/role-connections/metadata')
            self.export_data['role_connections_metadata'] = role_connections
            
            print(f"{Fore.GREEN}✓ Exported role connection metadata{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export role connections: {str(e)}{Style.RESET_ALL}")

    async def export_entitlements(self):
        """Export application entitlements"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export entitlements without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            application_id = self.export_data.get('application_info', {}).get('id')
            if not application_id and self.bot_id:
                application_id = self.bot_id
                
            if not application_id:
                print(f"{Fore.YELLOW}Cannot export entitlements without application ID.{Style.RESET_ALL}")
                return
                
            entitlements = await self.make_request(f'/applications/{application_id}/entitlements')
            self.export_data['entitlements'] = entitlements
            
            print(f"{Fore.GREEN}✓ Exported {len(entitlements)} entitlements{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export entitlements: {str(e)}{Style.RESET_ALL}")

    async def export_application_skus(self):
        """Export application SKUs"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export SKUs without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            application_id = self.export_data.get('application_info', {}).get('id')
            if not application_id and self.bot_id:
                application_id = self.bot_id
                
            if not application_id:
                print(f"{Fore.YELLOW}Cannot export SKUs without application ID.{Style.RESET_ALL}")
                return
                
            skus = await self.make_request(f'/applications/{application_id}/skus')
            self.export_data['skus'] = skus
            
            print(f"{Fore.GREEN}✓ Exported {len(skus)} SKUs{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export SKUs: {str(e)}{Style.RESET_ALL}")

    async def export_auth_url(self):
        """Generate authorization URL"""
        try:
            application_id = self.export_data.get('application_info', {}).get('id')
            if not application_id and self.bot_id:
                application_id = self.bot_id
                
            if not application_id:
                print(f"{Fore.YELLOW}Cannot generate auth URL without application ID.{Style.RESET_ALL}")
                return
            
            # Default OAuth2 scopes for bots
            default_scopes = [
                "bot", 
                "applications.commands"
            ]
            
            # Default permissions (Administrator)
            default_permissions = 8
            
            # Generate URL
            scope_string = "%20".join(default_scopes)
            auth_url = f"https://discord.com/api/oauth2/authorize?client_id={application_id}&permissions={default_permissions}&scope={scope_string}"
            
            self.export_data['auth_url'] = {
                "url": auth_url,
                "scopes": default_scopes,
                "permissions": default_permissions
            }
            
            print(f"{Fore.GREEN}✓ Generated authorization URL{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to generate auth URL: {str(e)}{Style.RESET_ALL}")

    async def export_member_counts(self):
        """Export member count statistics"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export member counts without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            member_counts = {}
            total_members = 0
            unique_members = set()
            
            detailed_guilds = self.export_data.get('detailed_guilds', [])
            for guild in detailed_guilds:
                guild_id = guild.get('id')
                member_count = guild.get('approximate_member_count', guild.get('member_count', 0))
                
                if guild_id:
                    member_counts[guild_id] = member_count
                    total_members += member_count
                    
                    # Try to get guild members to count unique members
                    try:
                        members = await self.make_request(f'/guilds/{guild_id}/members?limit=1000')
                        for member in members:
                            user_id = member.get('user', {}).get('id')
                            if user_id:
                                unique_members.add(user_id)
                    except:
                        # Fetching members might fail due to permissions, continue anyway
                        pass
                    
                    # Don't hit rate limits too hard
                    await asyncio.sleep(0.5)
            
            self.export_data['member_counts'] = {
                "guild_counts": member_counts,
                "total_members": total_members,
                "unique_members_found": len(unique_members)
            }
            
            print(f"{Fore.GREEN}✓ Exported member counts across {len(member_counts)} guilds{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export member counts: {str(e)}{Style.RESET_ALL}")

    async def export_message_stats(self):
        """Export message statistics (approximate)"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export message stats without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            message_stats = {
                "note": "Discord API doesn't provide historical message data easily. Limited sample only."
            }
            
            # Get a sample of messages from a few channels
            channel_messages = {}
            channels_sampled = 0
            total_messages = 0
            
            guild_channels = self.export_data.get('guild_channels', {})
            for guild_id, channels in guild_channels.items():
                # Only sample a few text channels per guild
                text_channels = [c for c in channels if c.get('type') == 0]  # 0 = text channel
                sample_channels = text_channels[:min(3, len(text_channels))]
                
                for channel in sample_channels:
                    channel_id = channel.get('id')
                    if channel_id:
                        messages = await self.make_request(f'/channels/{channel_id}/messages?limit=100')
                        if messages:
                            channel_messages[channel_id] = len(messages)
                            total_messages += len(messages)
                            channels_sampled += 1
                        
                        # Don't hit rate limits too hard
                        await asyncio.sleep(0.5)
                
                # Limit samples to prevent excessive API calls
                if channels_sampled >= 10:
                    break
            
            message_stats["sampled_channels"] = channel_messages
            message_stats["channels_sampled"] = channels_sampled
            message_stats["total_messages_sampled"] = total_messages
            
            self.export_data['message_stats'] = message_stats
            
            print(f"{Fore.GREEN}✓ Exported limited message statistics from {channels_sampled} channels{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export message stats: {str(e)}{Style.RESET_ALL}")

    async def export_gateway_info(self):
        """Export gateway connection information"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export gateway info without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            gateway_info = await self.make_request('/gateway/bot')
            self.export_data['gateway_info'] = gateway_info
            
            print(f"{Fore.GREEN}✓ Exported gateway connection information{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export gateway info: {str(e)}{Style.RESET_ALL}")

    async def export_application_assets(self):
        """Export application assets information"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export application assets without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            application_id = self.export_data.get('application_info', {}).get('id')
            if not application_id and self.bot_id:
                application_id = self.bot_id
                
            if not application_id:
                print(f"{Fore.YELLOW}Cannot export application assets without application ID.{Style.RESET_ALL}")
                return
            
            # Extract application icons/assets from the application info
            app_info = self.export_data.get('application_info', {})
            
            assets = {
                "icon": app_info.get("icon"),
                "cover_image": app_info.get("cover_image"),
                "asset_urls": []
            }
            
            # Generate asset URLs
            if assets["icon"]:
                icon_url = f"https://cdn.discordapp.com/app-icons/{application_id}/{assets['icon']}.png"
                assets["asset_urls"].append({"type": "icon", "url": icon_url})
                
            if assets["cover_image"]:
                cover_url = f"https://cdn.discordapp.com/app-assets/{application_id}/store/{assets['cover_image']}.png"
                assets["asset_urls"].append({"type": "cover_image", "url": cover_url})
            
            self.export_data['application_assets'] = assets
            
            print(f"{Fore.GREEN}✓ Exported application assets information{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export application assets: {str(e)}{Style.RESET_ALL}")

    async def export_bot_usage_stats(self):
        """Compile bot usage statistics summary"""
        try:
            stats = {
                "guilds": len(self.export_data.get('guilds', [])),
                "commands": len(self.export_data.get('global_commands', [])),
                "guild_specific_commands": sum(len(cmds) for cmds in self.export_data.get('guild_commands', {}).values()),
                "members_total": self.export_data.get('member_counts', {}).get('total_members', 0),
                "channels": sum(len(channels) for channels in self.export_data.get('guild_channels', {}).values()),
                "webhooks": sum(len(webhooks) for webhooks in self.export_data.get('guild_webhooks', {}).values()),
                "emojis": sum(len(emojis) for emojis in self.export_data.get('guild_emojis', {}).values()),
                "stickers": sum(len(stickers) for stickers in self.export_data.get('guild_stickers', {}).values()),
                "scheduled_events": sum(len(events) for events in self.export_data.get('guild_events', {}).values()),
                "roles": sum(len(roles) for roles in self.export_data.get('guild_roles', {}).values()),
                "integrations": sum(len(integrations) for integrations in self.export_data.get('guild_integrations', {}).values())
            }
            
            self.export_data['usage_stats_summary'] = stats
            
            print(f"{Fore.GREEN}✓ Compiled bot usage statistics summary{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to compile usage stats: {str(e)}{Style.RESET_ALL}")

    async def export_public_bot_info(self):
        """Attempt to find public information about the bot"""
        try:
            # This would typically use third-party services to find information
            # about bots, but we'll use a simple placeholder
            public_info = {
                "note": "This would typically check bot listing sites for public information",
                "bot_id": self.bot_id
            }
            
            self.export_data['public_info'] = public_info
            
            print(f"{Fore.YELLOW}Public bot information lookup not fully implemented{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export public bot info: {str(e)}{Style.RESET_ALL}")

    async def export_oauth2_info(self):
        """Export OAuth2 application information"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export OAuth2 info without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            # Most OAuth2 info is already in application_info
            oauth2_info = {
                "redirect_uris": self.export_data.get('application_info', {}).get('redirect_uris', []),
                "verify_key": self.export_data.get('application_info', {}).get('verify_key'),
                "terms_of_service_url": self.export_data.get('application_info', {}).get('terms_of_service_url'),
                "privacy_policy_url": self.export_data.get('application_info', {}).get('privacy_policy_url')
            }
            
            self.export_data['oauth2_info'] = oauth2_info
            
            print(f"{Fore.GREEN}✓ Exported OAuth2 application information{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export OAuth2 info: {str(e)}{Style.RESET_ALL}")

    async def export_connection_info(self):
        """Export connection information (bot connectivity)"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot export connection info without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            connection_info = {
                "gateway": self.export_data.get('gateway_info', {}),
                "api_version": 10,  # Current Discord API version
                "last_export_time": datetime.datetime.now().isoformat()
            }
            
            # Check for session limits
            gateway_info = self.export_data.get('gateway_info', {})
            session_start_limit = gateway_info.get('session_start_limit', {})
            if session_start_limit:
                connection_info['session_start_limit'] = session_start_limit
            
            self.export_data['connection_info'] = connection_info
            
            print(f"{Fore.GREEN}✓ Exported bot connection information{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export connection info: {str(e)}{Style.RESET_ALL}")

    async def export_intents_info(self):
        """Export intents information (based on bot capabilities)"""
        if not self.is_token_auth:
            print(f"{Fore.YELLOW}Cannot analyze intents without token authentication.{Style.RESET_ALL}")
            return
            
        try:
            # Analyze what intents the bot might be using based on the data it has access to
            intents_analysis = {
                "possible_intents": [],
                "note": "This is an estimation based on accessible data, not actual intent configuration"
            }
            
            # Check for guild member data
            if any(len(guild.get('members', [])) > 0 for guild in self.export_data.get('detailed_guilds', [])):
                intents_analysis["possible_intents"].append("GUILD_MEMBERS")
            
            # Check for presence data
            if any(len(guild.get('presences', [])) > 0 for guild in self.export_data.get('detailed_guilds', [])):
                intents_analysis["possible_intents"].append("GUILD_PRESENCES")
                
            # Check for message data
            if self.export_data.get('message_stats', {}).get('total_messages_sampled', 0) > 0:
                intents_analysis["possible_intents"].append("GUILD_MESSAGES")
                
            # More intent checks could be added
            
            self.export_data['intents_analysis'] = intents_analysis
            
            print(f"{Fore.GREEN}✓ Exported intents usage analysis{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to analyze intents: {str(e)}{Style.RESET_ALL}")

    async def export_rate_limit_info(self):
        """Export rate limit information"""
        try:
            rate_limits = {
                "global_limit": "50 requests per second per bot",
                "webhook_limit": "30 requests per minute per channel",
                "message_limit_normal": "5 messages per 5 seconds per user",
                "message_limit_burst": "5 messages per 2 seconds per user",
                "note": "These are standard Discord rate limits, not specific to this bot"
            }
            
            # Include any rate limit information from requests
            gateway_info = self.export_data.get('gateway_info', {})
            session_start_limit = gateway_info.get('session_start_limit', {})
            if session_start_limit:
                rate_limits['session_start_limit'] = session_start_limit
            
            self.export_data['rate_limits'] = rate_limits
            
            print(f"{Fore.GREEN}✓ Exported rate limit information{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to export rate limit info: {str(e)}{Style.RESET_ALL}")

    async def export_metadata(self):
        """Export metadata about the export process itself"""
        try:
            metadata = {
                "export_time": datetime.datetime.now().isoformat(),
                "exporter_version": "1.0.0",
                "discord_api_version": 10,
                "bot_id": self.bot_id,
                "export_method": "token" if self.is_token_auth else "bot_id",
                "export_components": list(self.export_data.keys())
            }
            
            self.export_data['metadata'] = metadata
            
            print(f"{Fore.GREEN}✓ Added export metadata{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to add metadata: {str(e)}{Style.RESET_ALL}")

    async def run_export(self):
        """Run the full export process with all enabled functions"""
        start_time = time.time()
        
        print(f"{Fore.CYAN}Starting Discord bot export...{Style.RESET_ALL}")
        
        # Basic info first
        await self.export_basic_info()
        
        # Main data export functions
        export_functions = [
            self.export_guilds,
            self.export_commands,
            self.export_permissions,
            self.export_channels,
            self.export_webhooks,
            self.export_interactions,
            self.export_presence,
            self.export_voice_settings,
            self.export_emoji,
            self.export_stickers,
            self.export_scheduled_events,
            self.export_roles,
            self.export_invites,
            self.export_bans,
            self.export_audit_logs,
            self.export_widget_settings,
            self.export_integrations,
            self.export_templates,
            self.export_welcome_screens,
            self.export_auto_moderation,
            self.export_stage_instances,
            self.export_application_role_connections,
            self.export_entitlements,
            self.export_application_skus,
            self.export_auth_url,
            self.export_member_counts,
            self.export_message_stats,
            self.export_gateway_info,
            self.export_application_assets,
            self.export_bot_usage_stats,
            self.export_public_bot_info,
            self.export_oauth2_info,
            self.export_connection_info,
            self.export_intents_info,
            self.export_rate_limit_info,
        ]
        
        # Execute all export functions
        for func in export_functions:
            await func()
        
        # Add metadata last
        await self.export_metadata()
        
        # Close the session
        await self.close_session()
        
        # Calculate duration
        duration = time.time() - start_time
        
        print(f"\n{Fore.GREEN}Export completed in {duration:.2f} seconds!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Exported {len(self.export_data)} data components.{Style.RESET_ALL}")
        
        return self.export_data

    def save_to_file(self, filename: str = None):
        """Save the exported data to a JSON file"""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            bot_identifier = self.bot_id if self.bot_id else "unknown"
            filename = f"discord_bot_export_{bot_identifier}_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.export_data, f, indent=2)
            
            print(f"{Fore.GREEN}Export saved to {filename}{Style.RESET_ALL}")
            return filename
        except Exception as e:
            print(f"{Fore.RED}Failed to save export: {str(e)}{Style.RESET_ALL}")
            return None


def print_discord_banner():
    """Print a fancy Discord-themed banner"""
    print(DISCORD_LOGO)

def list_all_functions():
    """Print all available functions in the exporter and utility tool"""
    # Export functions
    export_functions = [
        f"{Fore.LIGHTMAGENTA_EX}export_basic_info{Fore.RESET} - Export basic bot information",
        f"{Fore.LIGHTMAGENTA_EX}export_guilds{Fore.RESET} - Export all guilds the bot is in",
        f"{Fore.LIGHTMAGENTA_EX}export_commands{Fore.RESET} - Export all application commands",
        f"{Fore.LIGHTMAGENTA_EX}export_permissions{Fore.RESET} - Export permission settings",
        f"{Fore.LIGHTMAGENTA_EX}export_channels{Fore.RESET} - Export channels in guilds",
        f"{Fore.LIGHTMAGENTA_EX}export_webhooks{Fore.RESET} - Export webhook information",
        f"{Fore.LIGHTMAGENTA_EX}export_interactions{Fore.RESET} - Export recent interactions",
        f"{Fore.LIGHTMAGENTA_EX}export_presence{Fore.RESET} - Export presence configuration",
        f"{Fore.LIGHTMAGENTA_EX}export_voice_settings{Fore.RESET} - Export voice configuration",
        f"{Fore.LIGHTMAGENTA_EX}export_emoji{Fore.RESET} - Export custom emoji information",
        f"{Fore.LIGHTMAGENTA_EX}export_stickers{Fore.RESET} - Export custom sticker information",
        f"{Fore.LIGHTMAGENTA_EX}export_scheduled_events{Fore.RESET} - Export scheduled events",
        f"{Fore.LIGHTMAGENTA_EX}export_roles{Fore.RESET} - Export role configuration",
        f"{Fore.LIGHTMAGENTA_EX}export_invites{Fore.RESET} - Export active invites",
        f"{Fore.LIGHTMAGENTA_EX}export_bans{Fore.RESET} - Export ban lists",
        f"{Fore.LIGHTMAGENTA_EX}export_audit_logs{Fore.RESET} - Export recent audit logs",
        f"{Fore.LIGHTMAGENTA_EX}export_widget_settings{Fore.RESET} - Export widget configuration",
        f"{Fore.LIGHTMAGENTA_EX}export_integrations{Fore.RESET} - Export integrations information",
        f"{Fore.LIGHTMAGENTA_EX}export_templates{Fore.RESET} - Export guild templates",
        f"{Fore.LIGHTMAGENTA_EX}export_welcome_screens{Fore.RESET} - Export guild welcome screens",
        f"{Fore.LIGHTMAGENTA_EX}export_auto_moderation{Fore.RESET} - Export auto-moderation rules",
        f"{Fore.LIGHTMAGENTA_EX}export_stage_instances{Fore.RESET} - Export stage channel instances",
        f"{Fore.LIGHTMAGENTA_EX}export_application_role_connections{Fore.RESET} - Export role connections",
        f"{Fore.LIGHTMAGENTA_EX}export_entitlements{Fore.RESET} - Export application entitlements",
        f"{Fore.LIGHTMAGENTA_EX}export_application_skus{Fore.RESET} - Export application SKUs",
        f"{Fore.LIGHTMAGENTA_EX}export_auth_url{Fore.RESET} - Generate authorization URL",
        f"{Fore.LIGHTMAGENTA_EX}export_member_counts{Fore.RESET} - Export member count statistics",
        f"{Fore.LIGHTMAGENTA_EX}export_message_stats{Fore.RESET} - Export message statistics",
        f"{Fore.LIGHTMAGENTA_EX}export_gateway_info{Fore.RESET} - Export gateway connection information",
        f"{Fore.LIGHTMAGENTA_EX}export_application_assets{Fore.RESET} - Export application assets",
        f"{Fore.LIGHTMAGENTA_EX}export_bot_usage_stats{Fore.RESET} - Compile bot usage statistics",
        f"{Fore.LIGHTMAGENTA_EX}export_public_bot_info{Fore.RESET} - Find public information about the bot",
        f"{Fore.LIGHTMAGENTA_EX}export_oauth2_info{Fore.RESET} - Export OAuth2 application information",
        f"{Fore.LIGHTMAGENTA_EX}export_connection_info{Fore.RESET} - Export connection information",
        f"{Fore.LIGHTMAGENTA_EX}export_intents_info{Fore.RESET} - Export intents information",
        f"{Fore.LIGHTMAGENTA_EX}export_rate_limit_info{Fore.RESET} - Export rate limit information",
        f"{Fore.LIGHTMAGENTA_EX}export_metadata{Fore.RESET} - Export metadata about the export process"
    ]
    
    # Utility functions
    utility_functions = [
        f"{Fore.LIGHTBLUE_EX}create_text_channel{Fore.RESET} - Create a text channel in a guild",
        f"{Fore.LIGHTBLUE_EX}create_voice_channel{Fore.RESET} - Create a voice channel in a guild",
        f"{Fore.LIGHTBLUE_EX}create_category{Fore.RESET} - Create a category in a guild",
        f"{Fore.LIGHTBLUE_EX}create_role{Fore.RESET} - Create a role in a guild",
        f"{Fore.LIGHTBLUE_EX}create_emoji{Fore.RESET} - Create an emoji in a guild",
        f"{Fore.LIGHTBLUE_EX}send_message{Fore.RESET} - Send a message to a channel",
        f"{Fore.LIGHTBLUE_EX}get_messages{Fore.RESET} - Get messages from a channel",
        f"{Fore.LIGHTBLUE_EX}create_webhook{Fore.RESET} - Create a webhook for a channel",
        f"{Fore.LIGHTBLUE_EX}create_invite{Fore.RESET} - Create an invite for a channel",
        f"{Fore.LIGHTBLUE_EX}add_reaction{Fore.RESET} - Add a reaction to a message",
        f"{Fore.LIGHTBLUE_EX}create_thread{Fore.RESET} - Create a thread in a channel",
        f"{Fore.LIGHTBLUE_EX}pin_message{Fore.RESET} - Pin a message in a channel",
        f"{Fore.LIGHTBLUE_EX}create_slash_command{Fore.RESET} - Create a slash command",
        f"{Fore.LIGHTBLUE_EX}create_button_response{Fore.RESET} - Create a response with buttons",
        f"{Fore.LIGHTBLUE_EX}create_select_menu_response{Fore.RESET} - Create a response with a select menu",
        f"{Fore.LIGHTBLUE_EX}create_modal_response{Fore.RESET} - Create a modal response",
        f"{Fore.LIGHTBLUE_EX}update_bot_status{Fore.RESET} - Update bot status and activity",
        f"{Fore.LIGHTBLUE_EX}generate_embed{Fore.RESET} - Generate a Discord embed object",
        f"{Fore.LIGHTBLUE_EX}create_guild{Fore.RESET} - Create a new guild",
        f"{Fore.LIGHTBLUE_EX}create_guild_sticker{Fore.RESET} - Create a new sticker in a guild",
        f"{Fore.LIGHTBLUE_EX}create_scheduled_event{Fore.RESET} - Create a scheduled event in a guild",
        f"{Fore.LIGHTBLUE_EX}create_stage_instance{Fore.RESET} - Create a stage instance",
        f"{Fore.LIGHTBLUE_EX}create_dm_channel{Fore.RESET} - Create a DM channel with a user",
        f"{Fore.LIGHTBLUE_EX}create_group_dm{Fore.RESET} - Create a Group DM with multiple users",
        f"{Fore.LIGHTBLUE_EX}create_forum_thread{Fore.RESET} - Create a thread in a forum channel",
        f"{Fore.LIGHTBLUE_EX}create_auto_moderation_rule{Fore.RESET} - Create an auto moderation rule",
        f"{Fore.LIGHTBLUE_EX}create_application_command_permissions{Fore.RESET} - Set command permissions",
        f"{Fore.LIGHTBLUE_EX}create_guild_template{Fore.RESET} - Create a template from a guild",
        f"{Fore.LIGHTBLUE_EX}create_interaction_response{Fore.RESET} - Create a response to an interaction",
        f"{Fore.LIGHTBLUE_EX}create_message_component{Fore.RESET} - Create a message component",
        f"{Fore.LIGHTBLUE_EX}create_context_menu_command{Fore.RESET} - Create a context menu command",
        f"{Fore.LIGHTBLUE_EX}create_welcome_screen{Fore.RESET} - Configure the welcome screen for a guild",
        f"{Fore.LIGHTBLUE_EX}create_webhook_message{Fore.RESET} - Send a message through a webhook",
        f"{Fore.LIGHTBLUE_EX}add_guild_member_role{Fore.RESET} - Add a role to a guild member",
        f"{Fore.LIGHTBLUE_EX}remove_guild_member_role{Fore.RESET} - Remove a role from a guild member",
        f"{Fore.LIGHTBLUE_EX}create_guild_ban{Fore.RESET} - Ban a user from a guild",
        f"{Fore.LIGHTBLUE_EX}get_pinned_messages{Fore.RESET} - Get pinned messages from a channel"
    ]
    
    print(f"\n{Fore.CYAN}========== EXPORT FUNCTIONS ({len(export_functions)}) =========={Fore.RESET}")
    for func in export_functions:
        print(f"  {Fore.LIGHTBLUE_EX}•{Fore.RESET} {func}")
    
    print(f"\n{Fore.CYAN}========== UTILITY FUNCTIONS ({len(utility_functions)}) =========={Fore.RESET}")
    for func in utility_functions:
        print(f"  {Fore.LIGHTBLUE_EX}•{Fore.RESET} {func}")
    
    print(f"\n{Fore.CYAN}=================================================={Fore.RESET}")

async def main():
    """Main entry point for the Discord Bot Exporter tool"""
    
    # Check if -h or -H or --list-functions are provided directly 
    if any(arg in sys.argv for arg in ["-h", "-H", "--list-functions"]) and len(sys.argv) <= 3:
        print_discord_banner()
        list_all_functions()
        return
    
    parser = argparse.ArgumentParser(description="Discord Bot Data Exporter")
    
    auth_group = parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument("-t", "--token", help="Bot token for comprehensive export")
    auth_group.add_argument("-id", "--botid", help="Bot ID for basic export")
    auth_group.add_argument("-H", "--list-functions", action="store_true", help="List all available functions")
    
    parser.add_argument("-o", "--output", help="Output file name (default: auto-generated)")
    parser.add_argument("-f", "--function", help="Export specific function only")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode (less verbose output)")
    parser.add_argument("-p", "--pretty", action="store_true", help="Pretty print the JSON output")
    parser.add_argument("--no-save", action="store_true", help="Don't save to file, print to stdout instead")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    # Utility command arguments
    utility_group = parser.add_argument_group("Discord API Utility Commands")
    utility_group.add_argument("--create-channel", action="store_true", help="Create a text channel")
    utility_group.add_argument("--guild-id", help="Guild ID for commands that require it")
    utility_group.add_argument("--channel-id", help="Channel ID for commands that require it")
    utility_group.add_argument("--user-id", help="User ID for commands that require it")
    utility_group.add_argument("--message-id", help="Message ID for commands that require it")
    utility_group.add_argument("--application-id", help="Application ID for commands that require it")
    utility_group.add_argument("--name", help="Name parameter for creation commands")
    utility_group.add_argument("--description", help="Description for commands that require it")
    utility_group.add_argument("--content", help="Content/text for message sending commands")
    utility_group.add_argument("--channel-type", choices=["text", "voice", "category", "forum", "announcement"], 
                             default="text", help="Channel type to create")
    utility_group.add_argument("--create-role", action="store_true", help="Create a role in a guild")
    utility_group.add_argument("--send-message", action="store_true", help="Send a message to a channel")
    utility_group.add_argument("--create-webhook", action="store_true", help="Create a webhook for a channel")
    utility_group.add_argument("--create-invite", action="store_true", help="Create an invite for a channel")
    utility_group.add_argument("--create-slash-command", action="store_true", help="Create a slash command")
    utility_group.add_argument("--create-thread", action="store_true", help="Create a thread")
    utility_group.add_argument("--pin-message", action="store_true", help="Pin a message")
    utility_group.add_argument("--add-reaction", action="store_true", help="Add a reaction to a message")
    utility_group.add_argument("--emoji", help="Emoji for reaction commands")
    utility_group.add_argument("--color", type=int, default=0, help="Color integer for role creation")
    utility_group.add_argument("--topic", help="Topic for channel or stage creation")
    utility_group.add_argument("--create-dm", action="store_true", help="Create a DM channel with a user")
    utility_group.add_argument("--max-age", type=int, default=86400, help="Max age for invites in seconds")
    utility_group.add_argument("--max-uses", type=int, default=0, help="Max uses for invites (0 = unlimited)")
    utility_group.add_argument("--temporary", action="store_true", help="Whether the invite is temporary")
    utility_group.add_argument("--mentionable", action="store_true", help="Whether the role is mentionable")
    utility_group.add_argument("--hoist", action="store_true", help="Whether the role appears separated")
    utility_group.add_argument("--bitrate", type=int, default=64000, help="Bitrate for voice channels")
    utility_group.add_argument("--user-limit", type=int, default=0, help="User limit for voice channels (0 = unlimited)")
    utility_group.add_argument("--category-id", help="Parent category ID for channel creation")
    utility_group.add_argument("--image-url", help="URL to an image for commands that require it")
    utility_group.add_argument("--add-role", action="store_true", help="Add a role to a user")
    utility_group.add_argument("--remove-role", action="store_true", help="Remove a role from a user")
    utility_group.add_argument("--role-id", help="Role ID for role operations")
    utility_group.add_argument("--create-stage", action="store_true", help="Create a stage instance")
    utility_group.add_argument("--create-event", action="store_true", help="Create a scheduled event")
    utility_group.add_argument("--start-time", help="Start time for scheduled events (ISO format)")
    utility_group.add_argument("--end-time", help="End time for scheduled events (ISO format)")
    utility_group.add_argument("--location", help="Location for external scheduled events")
    utility_group.add_argument("--create-embed", action="store_true", help="Create and send an embed message")
    utility_group.add_argument("--embed-title", help="Title for embed messages")
    utility_group.add_argument("--embed-desc", help="Description for embed messages")
    utility_group.add_argument("--embed-color", type=int, default=0x5865F2, help="Color for embed messages (hex int)")
    utility_group.add_argument("--embed-image", help="Image URL for embed messages")
    utility_group.add_argument("--embed-thumbnail", help="Thumbnail URL for embed messages")
    utility_group.add_argument("--create-ban", action="store_true", help="Ban a user from a guild")
    utility_group.add_argument("--ban-delete-days", type=int, default=0, help="Number of days to delete messages for bans")
    utility_group.add_argument("--ban-reason", help="Reason for banning a user")
    
    args = parser.parse_args()
    
    # Check if the user wants to list all functions
    if args.list_functions:
        print_discord_banner()
        list_all_functions()
        return
    
    # Set up exporter
    exporter = DiscordExporter()
    
    # Set authentication method
    if args.token:
        exporter.set_token(args.token)
        print(f"{get_random_symbol()} {Fore.CYAN}Using token authentication for comprehensive export{Style.RESET_ALL}")
    elif args.botid:
        exporter.set_bot_id(args.botid)
        print(f"{get_random_symbol()} {Fore.CYAN}Using bot ID {args.botid} for limited export{Style.RESET_ALL}")
    
    # Check for utility commands
    utility_command_used = False
    
    # Handle channel creation
    if args.create_channel and args.token and args.guild_id and args.name:
        utility_command_used = True
        if args.channel_type == "text":
            result = await create_text_channel(
                exporter, 
                args.guild_id, 
                args.name,
                args.topic,
                args.category_id
            )
            if not args.no_save and result:
                with open(f"channel_{args.name}.json", "w") as f:
                    json.dump(result, f, indent=4)
        elif args.channel_type == "voice":
            result = await create_voice_channel(
                exporter, 
                args.guild_id, 
                args.name,
                args.bitrate,
                args.user_limit,
                args.category_id
            )
            if not args.no_save and result:
                with open(f"voice_channel_{args.name}.json", "w") as f:
                    json.dump(result, f, indent=4)
        elif args.channel_type == "category":
            result = await create_category(
                exporter, 
                args.guild_id, 
                args.name
            )
            if not args.no_save and result:
                with open(f"category_{args.name}.json", "w") as f:
                    json.dump(result, f, indent=4)
    
    # Handle role creation
    if args.create_role and args.token and args.guild_id and args.name:
        utility_command_used = True
        result = await create_role(
            exporter, 
            args.guild_id, 
            args.name,
            args.color,
            args.hoist,
            args.mentionable
        )
        if not args.no_save and result:
            with open(f"role_{args.name}.json", "w") as f:
                json.dump(result, f, indent=4)
    
    # Handle message sending
    if args.send_message and args.token and args.channel_id and args.content:
        utility_command_used = True
        embed = None
        if args.create_embed:
            embed = await generate_embed(
                title=args.embed_title,
                description=args.embed_desc,
                color=args.embed_color,
                image=args.embed_image,
                thumbnail=args.embed_thumbnail
            )
        result = await send_message(
            exporter, 
            args.channel_id, 
            args.content,
            embed
        )
        if not args.no_save and result:
            with open(f"message_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json", "w") as f:
                json.dump(result, f, indent=4)
    
    # Handle webhook creation
    if args.create_webhook and args.token and args.channel_id and args.name:
        utility_command_used = True
        result = await create_webhook(
            exporter, 
            args.channel_id, 
            args.name,
            args.image_url
        )
        if not args.no_save and result:
            with open(f"webhook_{args.name}.json", "w") as f:
                json.dump(result, f, indent=4)
    
    # Handle invite creation
    if args.create_invite and args.token and args.channel_id:
        utility_command_used = True
        result = await create_invite(
            exporter, 
            args.channel_id, 
            args.max_age,
            args.max_uses,
            args.temporary
        )
        if not args.no_save and result:
            with open(f"invite_{args.channel_id}.json", "w") as f:
                json.dump(result, f, indent=4)
            print(f"Invite URL: https://discord.gg/{result['code']}")
    
    # Handle reaction adding
    if args.add_reaction and args.token and args.channel_id and args.message_id and args.emoji:
        utility_command_used = True
        await add_reaction(
            exporter, 
            args.channel_id, 
            args.message_id,
            args.emoji
        )
    
    # Handle thread creation
    if args.create_thread and args.token and args.channel_id and args.name:
        utility_command_used = True
        result = await create_thread(
            exporter, 
            args.channel_id, 
            args.name,
            args.message_id
        )
        if not args.no_save and result:
            with open(f"thread_{args.name}.json", "w") as f:
                json.dump(result, f, indent=4)
    
    # Handle pinning message
    if args.pin_message and args.token and args.channel_id and args.message_id:
        utility_command_used = True
        await pin_message(
            exporter, 
            args.channel_id, 
            args.message_id
        )
    
    # Handle slash command creation
    if args.create_slash_command and args.token and args.application_id and args.name and args.description:
        utility_command_used = True
        result = await create_slash_command(
            exporter, 
            args.application_id, 
            args.name,
            args.description,
            None,
            args.guild_id
        )
        if not args.no_save and result:
            with open(f"slash_command_{args.name}.json", "w") as f:
                json.dump(result, f, indent=4)
                
    # Handle role operations
    if args.add_role and args.token and args.guild_id and args.user_id and args.role_id:
        utility_command_used = True
        await add_guild_member_role(
            exporter, 
            args.guild_id, 
            args.user_id,
            args.role_id
        )
        
    if args.remove_role and args.token and args.guild_id and args.user_id and args.role_id:
        utility_command_used = True
        await remove_guild_member_role(
            exporter, 
            args.guild_id, 
            args.user_id,
            args.role_id
        )
    
    # Handle DM creation
    if args.create_dm and args.token and args.user_id:
        utility_command_used = True
        result = await create_dm_channel(
            exporter, 
            args.user_id
        )
        if not args.no_save and result:
            with open(f"dm_channel_{args.user_id}.json", "w") as f:
                json.dump(result, f, indent=4)
    
    # Handle stage instance creation
    if args.create_stage and args.token and args.channel_id and args.topic:
        utility_command_used = True
        result = await create_stage_instance(
            exporter, 
            args.channel_id, 
            args.topic
        )
        if not args.no_save and result:
            with open(f"stage_{args.topic}.json", "w") as f:
                json.dump(result, f, indent=4)
    
    # Handle scheduled event creation
    if args.create_event and args.token and args.guild_id and args.name and args.description and args.start_time:
        utility_command_used = True
        result = await create_scheduled_event(
            exporter, 
            args.guild_id, 
            args.name,
            args.description,
            args.start_time,
            args.end_time,
            3,  # External event by default
            args.channel_id,
            args.location,
            args.image_url
        )
        if not args.no_save and result:
            with open(f"event_{args.name}.json", "w") as f:
                json.dump(result, f, indent=4)
    
    # Handle user banning
    if args.create_ban and args.token and args.guild_id and args.user_id:
        utility_command_used = True
        await create_guild_ban(
            exporter, 
            args.guild_id, 
            args.user_id,
            args.ban_delete_days,
            args.ban_reason
        )
    
    # Run normal export if no utility command was used
    if not utility_command_used:
        export_data = await exporter.run_export()
        
        # Handle output
        if not args.no_save:
            exporter.save_to_file(args.output)
        else:
            # Print to stdout
            indent = 2 if args.pretty else None
            print(json.dumps(export_data, indent=indent))

# ---- Discord Bot Utility Functions (Not Export Related) ----

async def add_guild_member_role(bot, guild_id: str, user_id: str, role_id: str):
    """Add a role to a guild member"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot add roles without token authentication.{Style.RESET_ALL}")
        return False
        
    try:
        # No body needed for this request
        await bot.make_request(
            f'/guilds/{guild_id}/members/{user_id}/roles/{role_id}', 
            "PUT"
        )
        
        print(f"{Fore.GREEN}✓ Added role {role_id} to user {user_id} in guild {guild_id}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error adding role: {str(e)}{Style.RESET_ALL}")
        return False

async def remove_guild_member_role(bot, guild_id: str, user_id: str, role_id: str):
    """Remove a role from a guild member"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot remove roles without token authentication.{Style.RESET_ALL}")
        return False
        
    try:
        # No body needed for this request
        await bot.make_request(
            f'/guilds/{guild_id}/members/{user_id}/roles/{role_id}', 
            "DELETE"
        )
        
        print(f"{Fore.GREEN}✓ Removed role {role_id} from user {user_id} in guild {guild_id}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error removing role: {str(e)}{Style.RESET_ALL}")
        return False

async def create_guild_ban(bot, guild_id: str, user_id: str, delete_message_days: int = 0, reason: str = None):
    """Ban a user from a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot ban users without token authentication.{Style.RESET_ALL}")
        return False
        
    try:
        data = {
            "delete_message_days": delete_message_days
        }
        
        if reason:
            data["reason"] = reason
            
        await bot.make_request(
            f'/guilds/{guild_id}/bans/{user_id}', 
            "PUT",
            data
        )
        
        print(f"{Fore.GREEN}✓ Banned user {user_id} from guild {guild_id}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error banning user: {str(e)}{Style.RESET_ALL}")
        return False

async def get_pinned_messages(bot, channel_id: str):
    """Get pinned messages from a channel"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot get pinned messages without token authentication.{Style.RESET_ALL}")
        return []
        
    try:
        response = await bot.make_request(f'/channels/{channel_id}/pins')
        
        if response:
            print(f"{Fore.GREEN}✓ Retrieved {len(response)} pinned messages from channel {channel_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to get pinned messages{Style.RESET_ALL}")
            return []
    except Exception as e:
        print(f"{Fore.RED}Error getting pinned messages: {str(e)}{Style.RESET_ALL}")
        return []

async def create_text_channel(bot, guild_id: str, name: str, topic: str = None, category_id: str = None):
    """Create a new text channel in a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create channels without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "type": 0,  # Text channel
            "permission_overwrites": []
        }
        
        if topic:
            data["topic"] = topic
            
        if category_id:
            data["parent_id"] = category_id
            
        response = await bot.make_request(f'/guilds/{guild_id}/channels', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created text channel '{name}' in guild {guild_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create text channel{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating text channel: {str(e)}{Style.RESET_ALL}")
        return None

async def create_voice_channel(bot, guild_id: str, name: str, bitrate: int = 64000, user_limit: int = 0, category_id: str = None):
    """Create a new voice channel in a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create channels without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "type": 2,  # Voice channel
            "bitrate": bitrate,
            "user_limit": user_limit,
            "permission_overwrites": []
        }
        
        if category_id:
            data["parent_id"] = category_id
            
        response = await bot.make_request(f'/guilds/{guild_id}/channels', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created voice channel '{name}' in guild {guild_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create voice channel{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating voice channel: {str(e)}{Style.RESET_ALL}")
        return None

async def create_category(bot, guild_id: str, name: str):
    """Create a new category in a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create categories without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "type": 4,  # Category
            "permission_overwrites": []
        }
            
        response = await bot.make_request(f'/guilds/{guild_id}/channels', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created category '{name}' in guild {guild_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create category{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating category: {str(e)}{Style.RESET_ALL}")
        return None

async def create_role(bot, guild_id: str, name: str, color: int = 0, hoist: bool = False, mentionable: bool = False):
    """Create a new role in a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create roles without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "color": color,
            "hoist": hoist,
            "mentionable": mentionable
        }
            
        response = await bot.make_request(f'/guilds/{guild_id}/roles', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created role '{name}' in guild {guild_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create role{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating role: {str(e)}{Style.RESET_ALL}")
        return None

async def create_emoji(bot, guild_id: str, name: str, image_data: str):
    """Create a new emoji in a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create emojis without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "image": image_data
        }
            
        response = await bot.make_request(f'/guilds/{guild_id}/emojis', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created emoji '{name}' in guild {guild_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create emoji{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating emoji: {str(e)}{Style.RESET_ALL}")
        return None

async def send_message(bot, channel_id: str, content: str, embed: Dict = None, tts: bool = False):
    """Send a message to a channel"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot send messages without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "content": content,
            "tts": tts
        }
        
        if embed:
            data["embeds"] = [embed]
            
        response = await bot.make_request(f'/channels/{channel_id}/messages', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Sent message to channel {channel_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to send message{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error sending message: {str(e)}{Style.RESET_ALL}")
        return None
        
async def get_messages(bot, channel_id: str, limit: int = 100):
    """Get messages from a channel"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot get messages without token authentication.{Style.RESET_ALL}")
        return []
        
    try:
        response = await bot.make_request(f'/channels/{channel_id}/messages?limit={limit}')
        
        if response:
            print(f"{Fore.GREEN}✓ Retrieved {len(response)} messages from channel {channel_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to get messages{Style.RESET_ALL}")
            return []
    except Exception as e:
        print(f"{Fore.RED}Error getting messages: {str(e)}{Style.RESET_ALL}")
        return []

async def create_webhook(bot, channel_id: str, name: str, avatar_url: str = None):
    """Create a webhook for a channel"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create webhooks without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name
        }
        
        if avatar_url:
            # Download avatar and convert to base64
            async with bot.session.get(avatar_url) as resp:
                if resp.status == 200:
                    avatar_bytes = await resp.read()
                    avatar_b64 = base64.b64encode(avatar_bytes).decode('utf-8')
                    data["avatar"] = f"data:image/png;base64,{avatar_b64}"
            
        response = await bot.make_request(f'/channels/{channel_id}/webhooks', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created webhook '{name}' for channel {channel_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create webhook{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating webhook: {str(e)}{Style.RESET_ALL}")
        return None

async def create_invite(bot, channel_id: str, max_age: int = 86400, max_uses: int = 0, temporary: bool = False, unique: bool = True):
    """Create an invite for a channel"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create invites without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "max_age": max_age,
            "max_uses": max_uses,
            "temporary": temporary,
            "unique": unique
        }
            
        response = await bot.make_request(f'/channels/{channel_id}/invites', "POST", data)
        
        if response and 'code' in response:
            print(f"{Fore.GREEN}✓ Created invite for channel {channel_id}: https://discord.gg/{response['code']}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create invite{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating invite: {str(e)}{Style.RESET_ALL}")
        return None

async def add_reaction(bot, channel_id: str, message_id: str, emoji: str):
    """Add a reaction to a message"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot add reactions without token authentication.{Style.RESET_ALL}")
        return False
        
    try:
        # URL encode the emoji
        encoded_emoji = urllib.parse.quote(emoji)
        
        response = await bot.make_request(
            f'/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me', 
            "PUT"
        )
        
        # Success returns 204 No Content
        print(f"{Fore.GREEN}✓ Added reaction {emoji} to message {message_id}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error adding reaction: {str(e)}{Style.RESET_ALL}")
        return False
        
async def create_thread(bot, channel_id: str, name: str, message_id: str = None, auto_archive_duration: int = 1440):
    """Create a thread in a channel"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create threads without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "auto_archive_duration": auto_archive_duration
        }
        
        if message_id:
            # Create thread from message
            response = await bot.make_request(
                f'/channels/{channel_id}/messages/{message_id}/threads', 
                "POST", 
                data
            )
        else:
            # Create thread without message
            response = await bot.make_request(
                f'/channels/{channel_id}/threads', 
                "POST", 
                data
            )
            
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created thread '{name}' in channel {channel_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create thread{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating thread: {str(e)}{Style.RESET_ALL}")
        return None
        
async def pin_message(bot, channel_id: str, message_id: str):
    """Pin a message in a channel"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot pin messages without token authentication.{Style.RESET_ALL}")
        return False
        
    try:            
        response = await bot.make_request(
            f'/channels/{channel_id}/pins/{message_id}', 
            "PUT"
        )
        
        # Success returns 204 No Content
        print(f"{Fore.GREEN}✓ Pinned message {message_id} in channel {channel_id}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error pinning message: {str(e)}{Style.RESET_ALL}")
        return False
        
async def create_slash_command(bot, application_id: str, name: str, description: str, options: List = None, guild_id: str = None):
    """Create a slash command"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create slash commands without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "description": description,
            "type": 1  # CHAT_INPUT
        }
        
        if options:
            data["options"] = options
            
        # Create global or guild command
        if guild_id:
            response = await bot.make_request(
                f'/applications/{application_id}/guilds/{guild_id}/commands', 
                "POST", 
                data
            )
        else:
            response = await bot.make_request(
                f'/applications/{application_id}/commands', 
                "POST", 
                data
            )
            
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created slash command '/{name}'{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create slash command{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating slash command: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_button_response(bot, interaction_id: str, interaction_token: str, content: str, components: List = None):
    """Create a response to an interaction with buttons"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot respond to interactions without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
            "data": {
                "content": content
            }
        }
        
        if components:
            data["data"]["components"] = components
            
        response = await bot.make_request(
            f'/interactions/{interaction_id}/{interaction_token}/callback', 
            "POST", 
            data
        )
        
        # Success returns 204 No Content
        print(f"{Fore.GREEN}✓ Sent interaction response with buttons{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error responding to interaction: {str(e)}{Style.RESET_ALL}")
        return False
        
async def create_select_menu_response(bot, interaction_id: str, interaction_token: str, content: str, options: List):
    """Create a response to an interaction with a select menu"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot respond to interactions without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
            "data": {
                "content": content,
                "components": [
                    {
                        "type": 1,  # ACTION_ROW
                        "components": [
                            {
                                "type": 3,  # SELECT_MENU
                                "custom_id": "select_menu",
                                "options": options
                            }
                        ]
                    }
                ]
            }
        }
            
        response = await bot.make_request(
            f'/interactions/{interaction_id}/{interaction_token}/callback', 
            "POST", 
            data
        )
        
        # Success returns 204 No Content
        print(f"{Fore.GREEN}✓ Sent interaction response with select menu{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error responding to interaction: {str(e)}{Style.RESET_ALL}")
        return False
        
async def create_modal_response(bot, interaction_id: str, interaction_token: str, title: str, custom_id: str, components: List):
    """Create a modal response to an interaction"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot respond with modals without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "type": 9,  # MODAL
            "data": {
                "title": title,
                "custom_id": custom_id,
                "components": components
            }
        }
            
        response = await bot.make_request(
            f'/interactions/{interaction_id}/{interaction_token}/callback', 
            "POST", 
            data
        )
        
        # Success returns 204 No Content
        print(f"{Fore.GREEN}✓ Sent modal response{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error responding with modal: {str(e)}{Style.RESET_ALL}")
        return False
        
async def update_bot_status(bot, status: str, activity_type: int = 0, activity_name: str = None):
    """Update bot status and activity"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot update status without token authentication.{Style.RESET_ALL}")
        return False
        
    try:
        data = {
            "op": 3,  # Presence Update
            "d": {
                "since": None,
                "activities": [],
                "status": status,
                "afk": False
            }
        }
        
        if activity_name:
            data["d"]["activities"].append({
                "name": activity_name,
                "type": activity_type
            })
            
        # This is not a REST API call, but a gateway payload
        # For simplicity, we're just showing the data that would be sent
        print(f"{Fore.GREEN}✓ Status update prepared (requires gateway connection to apply):{Style.RESET_ALL}")
        print(json.dumps(data, indent=2))
        return data
    except Exception as e:
        print(f"{Fore.RED}Error preparing status update: {str(e)}{Style.RESET_ALL}")
        return False
        
async def generate_embed(title: str = None, description: str = None, url: str = None, 
                        color: int = None, fields: List = None, author: Dict = None,
                        footer: Dict = None, image: str = None, thumbnail: str = None):
    """Generate a Discord embed object"""
    try:
        embed = {}
        
        if title:
            embed["title"] = title
        
        if description:
            embed["description"] = description
            
        if url:
            embed["url"] = url
            
        if color:
            embed["color"] = color
            
        if fields:
            embed["fields"] = fields
            
        if author:
            embed["author"] = author
            
        if footer:
            embed["footer"] = footer
            
        if image:
            embed["image"] = {"url": image}
            
        if thumbnail:
            embed["thumbnail"] = {"url": thumbnail}
            
        return embed
    except Exception as e:
        print(f"{Fore.RED}Error generating embed: {str(e)}{Style.RESET_ALL}")
        return {}
        
async def create_guild(bot, name: str, region: str = None, icon_data: str = None):
    """Create a new guild (server)"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create guilds without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name
        }
        
        if region:
            data["region"] = region
            
        if icon_data:
            data["icon"] = icon_data
            
        response = await bot.make_request(f'/guilds', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created guild '{name}'{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create guild{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating guild: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_guild_sticker(bot, guild_id: str, name: str, description: str, tags: str, file_data: str):
    """Create a new sticker in a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create stickers without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "description": description,
            "tags": tags,
            "file": file_data
        }
            
        response = await bot.make_request(f'/guilds/{guild_id}/stickers', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created sticker '{name}' in guild {guild_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create sticker{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating sticker: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_scheduled_event(bot, guild_id: str, name: str, description: str, 
                               start_time: str, end_time: str = None, 
                               entity_type: int = 3, channel_id: str = None, 
                               location: str = None, image: str = None):
    """Create a scheduled event in a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create scheduled events without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "description": description,
            "scheduled_start_time": start_time,
            "entity_type": entity_type,
            "privacy_level": 2  # GUILD_ONLY
        }
        
        if end_time:
            data["scheduled_end_time"] = end_time
            
        if entity_type == 1:  # STAGE_INSTANCE
            if not channel_id:
                raise ValueError("Channel ID required for stage instance events")
            data["channel_id"] = channel_id
        elif entity_type == 2:  # VOICE
            if not channel_id:
                raise ValueError("Channel ID required for voice events")
            data["channel_id"] = channel_id
        elif entity_type == 3:  # EXTERNAL
            if not location:
                raise ValueError("Location required for external events")
            data["entity_metadata"] = {"location": location}
            
        if image:
            data["image"] = image
            
        response = await bot.make_request(f'/guilds/{guild_id}/scheduled-events', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created scheduled event '{name}' in guild {guild_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create scheduled event{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating scheduled event: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_stage_instance(bot, channel_id: str, topic: str, privacy_level: int = 1):
    """Create a stage instance"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create stage instances without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "channel_id": channel_id,
            "topic": topic,
            "privacy_level": privacy_level
        }
            
        response = await bot.make_request(f'/stage-instances', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created stage instance with topic '{topic}'{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create stage instance{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating stage instance: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_dm_channel(bot, recipient_id: str):
    """Create a DM channel with a user"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create DMs without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "recipient_id": recipient_id
        }
            
        response = await bot.make_request('/users/@me/channels', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created DM channel with user {recipient_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create DM channel{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating DM channel: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_group_dm(bot, access_tokens: List[str], nicks: Dict[str, str]):
    """Create a Group DM with multiple users"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create Group DMs without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "access_tokens": access_tokens,
            "nicks": nicks
        }
            
        response = await bot.make_request('/users/@me/channels', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created Group DM with {len(access_tokens)} users{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create Group DM{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating Group DM: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_forum_thread(bot, channel_id: str, name: str, message: Dict, applied_tags: List[str] = None):
    """Create a thread in a forum channel"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create forum threads without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "message": message
        }
        
        if applied_tags:
            data["applied_tags"] = applied_tags
            
        response = await bot.make_request(f'/channels/{channel_id}/threads', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created forum thread '{name}' in channel {channel_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create forum thread{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating forum thread: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_auto_moderation_rule(bot, guild_id: str, name: str, event_type: int, 
                                    trigger_type: int, trigger_metadata: Dict, 
                                    actions: List[Dict], enabled: bool = True,
                                    exempt_roles: List[str] = None, 
                                    exempt_channels: List[str] = None):
    """Create an auto moderation rule in a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create auto moderation rules without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "event_type": event_type,
            "trigger_type": trigger_type,
            "trigger_metadata": trigger_metadata,
            "actions": actions,
            "enabled": enabled
        }
        
        if exempt_roles:
            data["exempt_roles"] = exempt_roles
            
        if exempt_channels:
            data["exempt_channels"] = exempt_channels
            
        response = await bot.make_request(f'/guilds/{guild_id}/auto-moderation/rules', "POST", data)
        
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created auto moderation rule '{name}' in guild {guild_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create auto moderation rule{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating auto moderation rule: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_application_command_permissions(bot, application_id: str, guild_id: str, 
                                               command_id: str, permissions: List[Dict]):
    """Set permissions for an application command in a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot set command permissions without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "permissions": permissions
        }
            
        response = await bot.make_request(
            f'/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions', 
            "PUT", 
            data
        )
        
        if response:
            print(f"{Fore.GREEN}✓ Set permissions for command {command_id} in guild {guild_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to set command permissions{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error setting command permissions: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_guild_template(bot, guild_id: str, name: str, description: str = None):
    """Create a template from a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create templates without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name
        }
        
        if description:
            data["description"] = description
            
        response = await bot.make_request(f'/guilds/{guild_id}/templates', "POST", data)
        
        if response and 'code' in response:
            print(f"{Fore.GREEN}✓ Created template '{name}' from guild {guild_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create template{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating template: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_interaction_response(bot, interaction_id: str, interaction_token: str, 
                                    type: int, data: Dict = None):
    """Create a response to an interaction"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot respond to interactions without token authentication.{Style.RESET_ALL}")
        return False
        
    try:
        payload = {
            "type": type
        }
        
        if data:
            payload["data"] = data
            
        response = await bot.make_request(
            f'/interactions/{interaction_id}/{interaction_token}/callback', 
            "POST", 
            payload
        )
        
        # Success returns 204 No Content
        print(f"{Fore.GREEN}✓ Sent interaction response type {type}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error responding to interaction: {str(e)}{Style.RESET_ALL}")
        return False
        
async def create_message_component(component_type: int, custom_id: str = None, style: int = None, 
                                 label: str = None, emoji: Dict = None, url: str = None, 
                                 options: List = None, placeholder: str = None, 
                                 min_values: int = None, max_values: int = None, 
                                 components: List = None):
    """Create a message component (button, select menu, etc.)"""
    try:
        component = {
            "type": component_type
        }
        
        if custom_id:
            component["custom_id"] = custom_id
            
        if style:
            component["style"] = style
            
        if label:
            component["label"] = label
            
        if emoji:
            component["emoji"] = emoji
            
        if url:
            component["url"] = url
            
        if options:
            component["options"] = options
            
        if placeholder:
            component["placeholder"] = placeholder
            
        if min_values is not None:
            component["min_values"] = min_values
            
        if max_values is not None:
            component["max_values"] = max_values
            
        if components:
            component["components"] = components
            
        return component
    except Exception as e:
        print(f"{Fore.RED}Error creating component: {str(e)}{Style.RESET_ALL}")
        return {}
        
async def create_context_menu_command(bot, application_id: str, name: str, type: int = 2, 
                                    guild_id: str = None):
    """Create a context menu command (user or message)"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot create context menu commands without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "name": name,
            "type": type  # 2 for USER, 3 for MESSAGE
        }
            
        # Create global or guild command
        if guild_id:
            response = await bot.make_request(
                f'/applications/{application_id}/guilds/{guild_id}/commands', 
                "POST", 
                data
            )
        else:
            response = await bot.make_request(
                f'/applications/{application_id}/commands', 
                "POST", 
                data
            )
            
        if response and 'id' in response:
            print(f"{Fore.GREEN}✓ Created context menu command '{name}'{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to create context menu command{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error creating context menu command: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_welcome_screen(bot, guild_id: str, enabled: bool = True, welcome_channels: List[Dict] = None, 
                              description: str = None):
    """Configure the welcome screen for a guild"""
    if not bot.is_token_auth:
        print(f"{Fore.YELLOW}Cannot configure welcome screen without token authentication.{Style.RESET_ALL}")
        return None
        
    try:
        data = {
            "enabled": enabled
        }
        
        if welcome_channels:
            data["welcome_channels"] = welcome_channels
            
        if description:
            data["description"] = description
            
        response = await bot.make_request(f'/guilds/{guild_id}/welcome-screen', "PATCH", data)
        
        if response:
            print(f"{Fore.GREEN}✓ Configured welcome screen for guild {guild_id}{Style.RESET_ALL}")
            return response
        else:
            print(f"{Fore.RED}Failed to configure welcome screen{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error configuring welcome screen: {str(e)}{Style.RESET_ALL}")
        return None
        
async def create_webhook_message(bot, webhook_id: str, webhook_token: str, content: str = None, 
                               username: str = None, avatar_url: str = None, tts: bool = None, 
                               embeds: List = None, allowed_mentions: Dict = None, 
                               components: List = None, thread_name: str = None):
    """Send a message through a webhook"""
    try:
        data = {}
        
        if content:
            data["content"] = content
            
        if username:
            data["username"] = username
            
        if avatar_url:
            data["avatar_url"] = avatar_url
            
        if tts is not None:
            data["tts"] = tts
            
        if embeds:
            data["embeds"] = embeds
            
        if allowed_mentions:
            data["allowed_mentions"] = allowed_mentions
            
        if components:
            data["components"] = components
            
        # Make request without using bot's token
        url = f"{API_ENDPOINT}/webhooks/{webhook_id}/{webhook_token}"
        
        # For thread creation
        if thread_name:
            url += f"?thread_name={urllib.parse.quote(thread_name)}"
            
        headers = {
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json"
        }
        
        if not bot.session:
            await bot.initialize_session()
            
        response = await bot.session.post(url, headers=headers, json=data)
        
        if response.status == 204:
            print(f"{Fore.GREEN}✓ Sent webhook message successfully{Style.RESET_ALL}")
            return True
        else:
            result = await response.json()
            if result and 'id' in result:
                print(f"{Fore.GREEN}✓ Sent webhook message successfully{Style.RESET_ALL}")
                return result
            else:
                print(f"{Fore.RED}Failed to send webhook message{Style.RESET_ALL}")
                return None
    except Exception as e:
        print(f"{Fore.RED}Error sending webhook message: {str(e)}{Style.RESET_ALL}")
        return None

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Export canceled by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
