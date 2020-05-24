import discord
from discord.ext import commands, tasks


class Help(commands.Cog, name="Help"):
    """The help command!"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx, *, category=None):
        """Gets all category and commands."""
        try:
            if category is None:
                """Category listing.  What more?"""
                halp = discord.Embed(title='All command categories',
                                     color=discord.Color.blue())
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('**{}** - {}'.format(x, self.bot.cogs[x].__doc__) + '\n')
                halp.add_field(name='Type `-help [Name]` for more info', value=cogs_desc[0:len(cogs_desc) - 1], inline=False)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name, y.help) + '\n')
                # halp.add_field(name='Un-categorized Commands', value=cmds_desc[0:len(cmds_desc) - 1], inline=False)
                # await ctx.message.add_reaction(emoji='✉')
                await ctx.send('', embed=halp)
            else:
                """Command listing within a category."""
                found = False
                for x in self.bot.cogs:
                    category = category.title()
                    if x == category:
                        halp = discord.Embed(title=category + ' Commands',
                                             description=self.bot.cogs[category].__doc__,
                                             color=discord.Color.blue())
                        for c in self.bot.get_cog(category).get_commands():
                            if not c.hidden:
                                params = []
                                paramsDict = list(c.clean_params.items())
                                for i in range(len(c.clean_params)):
                                    if str(paramsDict[i][1])[-5:] == "=None":
                                        params.append(f"[{str(paramsDict[i][0])}]")
                                    else:
                                        params.append(f"<{str(paramsDict[i][0])}>")
                                halp.add_field(name=f"**Command:** `{self.bot.command_prefix}{c.name}`",
                                               value=f"{c.help}",
                                               inline=False)
                        found = True
                if not found:
                    """Reminds you if that category doesn't exist."""
                    halp = discord.Embed(title='Error!', description='Did not recognize category "' + category + '"!',
                                         color=discord.Color.red())
                else:
                    # await ctx.message.add_reaction(emoji='✉')
                    pass
                await ctx.send(embed=halp)
        except ValueError:
            await ctx.send("Excuse me, I can't send embeds.")


def setup(bot):
    bot.add_cog(Help(bot))