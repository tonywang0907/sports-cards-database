from django.db import models

# Create your models here.
class SportsCard(models.Model):
    sport = models.CharField(max_length=100)
    player = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    variation = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    picture = models.ImageField(upload_to='card_pictures')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} {self.player} {self.variation}"


class Tag(models.Model):
    name = models.CharField(max_length=50)
    cards = models.ManyToManyField(SportsCard, through='TagCard')

    def __str__(self):
        return self.name


class TagCard(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    card = models.ForeignKey(SportsCard, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tag', 'card')

    def __str__(self):
        return f"{self.card.product} {self.card.player} {self.card.variation} - {self.tag.name}"