from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50)

class Game(models.Model):
    """
    Represents a game instance in a tic-tac-toe game.
    
    Attributes:
        date_created (DateTimeField): The date and time when the game was created.
        date_updated (DateTimeField): The date and time when the game was last updated.
        board (CharField): The state of the game board as a string.
        player_x (ForeignKey): The player with 'X' symbol.
        player_o (ForeignKey): The player with 'O' symbol.
        winner (ForeignKey): The winner of the game. Can be null if there is no winner yet.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    board = models.CharField(max_length=9, default=" " * 9)
    player_x = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='player_x_games')
    player_o = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='player_o_games')
    
    winner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_games')
    
    def __str__(self):
        """
        Returns a string representation of the game instance.
        
        Returns:
            str: A string showing the players and the state of the game board.
        """
        return f'{self.player_x} vs {self.player_o}, state="{self.board}"'

    @property
    def get_winner_name(self):
        """
        Returns the username of the winner if there is one, otherwise returns None.
        
        Returns:
            str or None: The username of the winner if there is one, otherwise None.
        """
        if self.winner:
            return self.winner.username
        return None

class Score(models.Model):
    player = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='score')
    total_games_played = models.PositiveIntegerField(default=0)
    games_won = models.PositiveIntegerField(default=0)
