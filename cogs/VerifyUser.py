from speedruncompy import GetUserSummary, NetworkId, SitePowerLevel
from datetime import datetime
from discord.ext import bridge, commands
from enum import Enum
from dateutil.relativedelta import relativedelta

# how many weeks to check for discord account server join date 
discordTimeCheckInSeconds = 2    

# discord role name
verifiedRoleName = "RoleNameHere"

# how many months to check for src account creation
monthCheck = 6

# SRC ID list for each game to be checked
gameList = ['game', 'ids', 'go', 'here']

class DiscordSocialLink(Enum):
    NoConnection = 0
    OldConnection = 1
    NoMatch = 2
    TrueConnection = 3


class Verify(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.Data = None
        self.currentTime = None
    
    # Comments
    @bridge.bridge_command(name="verify-user-src", description="Verify The User Via Their SRC Profile")
    async def SRCVerifyUser(self, ctx, src_username = None):
        
        # Already verified
        if any([role for role in ctx.author.roles if role.name == verifiedRoleName]):
            await ctx.respond("You are already verified.", ephemeral = True)
            return

        # no username provided
        if src_username == None:
            await ctx.respond("No username was provided.", ephemeral = True)
            return
        
        # try to pull data from src (username may not exist)
        try:
            self.Data = await GetUserSummary(url = src_username).perform_async()

        except Exception as e:
            await ctx.respond("User profile: \"" + src_username + "\" does not exist.", ephemeral = True)
            return
        
        # given speedrun username is currently banned on site
        if self.Data['user']['powerLevel'] == SitePowerLevel.BANNED:
            await ctx.respond("User profile: \"" + src_username + "\" is currently banned on Speedrun.com.", ephemeral = True)
            return

        # confirm if SRC account has discord social media link
        discordLinkStatus = self.SRCLinkCheck(ctx)

        # handle errors based on speedrun.com profile's discord social link
        match discordLinkStatus:

            case DiscordSocialLink.NoConnection:
                await ctx.respond("No discord social link exists for user profile: \"" + src_username + "\".", ephemeral = True)
                return
            
            case DiscordSocialLink.OldConnection:
                await ctx.respond("A discord social link exists for user profile: \"" + src_username + "\" - however, it references a legacy discord username.", ephemeral = True)
                return

            case DiscordSocialLink.NoMatch:
                await ctx.respond("A discord social link exists for user profile: \"" + src_username + "\" - however, it references a different discord username.", ephemeral = True)
                return

        # get verified role information
        roleID = [role for role in ctx.guild.roles if role.name == verifiedRoleName]

        # failed to find role
        if len(roleID) == 0:
            await ctx.respond("Can't find role to give verified users", ephemeral = True)
            return False

        # user's SRC account has existed for >=6 months
        if self.SRCSixMonthCheck():
            await ctx.respond("Verified: Six Months")
            await ctx.author.add_roles(roleID[0])
            return


        # user's SRC account has a verified run for atleast one of the required games
        if self.GameCheck():
            await ctx.respond("Verified: Runner")
            await ctx.author.add_roles(roleID[0])
            return


        # no verification criteria met
        await ctx.respond("You have not met any verification criteria.", ephemeral = True)
        return

    def SRCLinkCheck(self, ctx):
            
        # check for any social media links where networkId = discord
        socialMediaConnections = [item for item in self.Data['userSocialConnectionList'] if item['networkId'] == NetworkId.DISCORD]

        # no discord social link found
        if(len(socialMediaConnections) == 0):
            return DiscordSocialLink.NoConnection
        

        # get possible discriminator zone
        discriminator = (socialMediaConnections[0])['value'][-5:]

        # check if the first character of the last five is '#' and the rest are digits (old style username with discriminator)
        if discriminator[0] == '#' and discriminator[1:].isdigit():
            return DiscordSocialLink.OldConnection


        # is of new style, yet doesn't match current discord username
        if((socialMediaConnections[0])['value'] != ctx.author.name):
            return DiscordSocialLink.NoMatch
        

        # social link found and matches current discord username
        return DiscordSocialLink.TrueConnection

    def SRCSixMonthCheck(self):
    
        # Get the current date and time
        self.currentTime = datetime.now()
        
        # 6 months ago relative (i.e. December 31st -> June 30th, as 'June 31st' doesn't exist)
        newDate = self.currentTime - relativedelta(months=monthCheck)
        
        # if user signup epoch is greater than the epoch 6 months ago from exact current time, account is younger than 6 months (lower value = closer to Jan 1st. 1970)
        if self.Data['userProfile'].signupDate >= newDate.timestamp():
            return False
        
        return True
    
    def DiscordXWeekCheck(self, ctx):

        # Get the current date and time
        self.currentTime = datetime.now()

        # calculate date for x weeks ago
        xWeeksAgo = self.currentTime - relativedelta(weeks=2)

        # if joined date epoch is greater than the epoch x weeks ago from current time, then x weeks haven't passed (lower value = closer to Jan 1st. 1970)
        if ctx.author.joined_at.timestamp() > xWeeksAgo.timestamp():
            return False
        
        return True

    def GameCheck(self):
    
        # all game ids the SRC user has a verified run of that we are interested in (How do you get pending runs?)
        found_ids = [game['gameId'] for game in self.Data['userGameRunnerStats'] if game['gameId'] in gameList]
        
        # user hasn't had a run from any of the specified games verified
        if len(found_ids) == 0:
            return False
        
        return True



    @bridge.bridge_command(name="verify-user-discord", description="Verify The User Via Their Discord Join Date")
    async def DISVerifyUser(self, ctx):

        # get verified role information
        roleID = [role for role in ctx.guild.roles if role.name == verifiedRoleName]
        
        # Already has been verified
        if any([role for role in ctx.author.roles if role.name == verifiedRoleName]):
            await ctx.respond("You are already verified.", ephemeral = True)
            return
        
        # user has been in the discord server for >= x Weeks
        if self.DiscordXWeekCheck(ctx):
            await ctx.respond("Verified: Two Weeks Joined")
            await ctx.author.add_roles(roleID[0])
            return


def setup(client):
    client.add_cog(Verify(client))