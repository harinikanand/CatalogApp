#!/usr/bin/python
# -*- coding: utf-8 -*-

# The purpose of this file is to create a user
# and 5 genres with several books under them
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Book_genres, Base, Books, User

engine = create_engine('sqlite:///bookstore.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Harini Anand", email="harinikanand03@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# List for Genre 1
book_genre1 = Book_genres(user_id=1,name="Art")

session.add(book_genre1)
session.commit()

book1 = Books(user_id=1,name="Van Gogh's Flowers",
              description="Vincent van Gogh is one of the world's \
most renowned and influential artists. The story of his troubled life has long fascinated \
art lovers, shaping the way we view and interpret his work. But Van Gogh, the artist and \
the man, was also inspired by the beauty and colors of nature, and expressed his passion \
in some of the most vibrant depictions of the natural world ever put on canvas.",
              author="Debra N. Mancoff",
              price="$1.99",
              book_genre=book_genre1)

session.add(book1)
session.commit()


book2 = Books(user_id=1,name="Georgia O'Keeffe Museum Collection",
              description="Georgia O'Keeffe is one of \
the great artists of the twentieth century, and one of the best loved. The Georgia O'Keeffe Museum \
in Santa Fe, New Mexico, holds the largest collection of her work, her archives, and her houses at \
Ghost Ranch and in Abiquiu",
              author="Barbara Buhler Lynes, Georgia O'Keeffe",
              price="$45.88",
              book_genre=book_genre1)
session.add(book2)
session.commit()

book3 = Books(user_id=1,name="Salvador Dali: 1904-1989",
              description="A genius with a right to indulge in \
whatever lunacy popped into his head. Picasso called Dali an outboard motor that's always running.\
Dali thought himself a genius with a right to indulge in whatever lunacy popped into his head.\
Painter, sculptor, writer and film maker, Salvador Dali (1904 - 1989) was one of the century's \
greatest exhibitionists and eccentrics - and was rewarded with fierce controversy wherever he went.",
              author="Gilles Neret",
              price="$1.99",
              book_genre=book_genre1)
session.add(book3)
session.commit()

book4 = Books(user_id=1,name="Henri Matisse, 1869-1954: Master of Colour",
              description="Henri Matisse (1869-1954) is known not only as one of the most important \
French painters of the 20th century but also as co-founder and leading exponent of Fauvism",
              author="Volkmar Essers",
              price="$9.99",
              book_genre=book_genre1) 
session.add(book4)
session.commit()


# List for Genre 2
book_genre2 = Book_genres(user_id=1,name="Biography")

session.add(book_genre2)
session.commit()

book1 = Books(user_id=1,name="Eisenhower: A Biography",
              description="WWII expert John Wukovits explores Dwight D. Eisenhower's contributions to \
American warfare. American general and 34th president of the United States",
              author="John Wukovits",
              price="$9.19",
              book_genre=book_genre2)

session.add(book1)
session.commit()


book2 = Books(user_id=1,name="The Hills and The Vale",
              description="The Hills and The Vale",
              author="Richard Jefferies",
              price="$9.99",
              book_genre=book_genre2)
 
session.add(book2)
session.commit()
book3 = Books(user_id=1,name="Salvador Dali: 1904-1989",
              description="Award-winning author and journalist Tom Graves in\
 - Louise Brooks, Frank Zappa, & Other Charmers & Dreamers - collects the best of his long-form journalism and \
profiles as well as his in-depth interviews with a variety of curious personalities.",
              author="Tom Graves",
              price="$19.95",
              book_genre=book_genre2)
session.add(book3)
session.commit()

book4 = Books(user_id=1,name="The Universal Tone: Bringing My Story to Light",
              description="In 1967 at San Francisco's Fillmore Auditorium, a young guitarist played a \
blistering solo that announced a prodigious talent. Two years later he played a historic set at Woodstock,\
and the world came to know Carlos Santana by name.",
              author="Carlos Santana",
              price="$15.28",
              book_genre=book_genre2)
session.add(book4)
session.commit()

book5 = Books(user_id=1,name="Keep Moving: And Other Tips and Truths About Aging",
              description="Show-business legend Dick Van Dyke is living proof that life does get better the\
longer you live it",
              author="Dick Van Dyke, Todd Gold",
              price="$15.86",
              book_genre=book_genre2) 
session.add(book5)
session.commit()


# List for Genre 3
book_genre3 = Book_genres(user_id=1,name="Fiction")

session.add(book_genre3)
session.commit()

book1 = Books(user_id=1,name="Garden of Lies",
              description="A new mother's desperate decision sets in motion a dramatic series of events leading to an epic romance",
              author="Eileen Goudge",
              price="$7.49",
              book_genre=book_genre3)

session.add(book1)
session.commit()


book2 = Books(user_id=1,name="Rogue Lawyer",
              description="Sebastian Rudd is not your typical street lawyer. He works of \
of a customized bulletproof van, complete with Wi-Fi, a bar, a small fridge, fine leather chairs, a hidden gun \
compartment, and a heavily armed driver. He has no firm, no partners, no associates, and only one employee, his\
driver",
              author="John Grisham",
              price="$17.71",
              book_genre=book_genre3)
session.add(book2)
session.commit()

book3 = Books(user_id=1,name="All the Light We Cannot See",
	      description="From the highly acclaimed, multiple award-winning Anthony Doerr, the beautiful,stunningly \
ambitious instant New York Times bestseller about a blind French girl and a German boy whose paths collide in occupied \
France as both try to survive the devastation of World War II.",
              author="Anthony Doerr",
              price="$15.90",
              book_genre=book_genre3)

session.add(book3)
session.commit()

book4 = Books(user_id=1,name="Go Set a Watchman",
              description="Twenty-six-year-old Jean Louise Finch Scout returns home from New York City to visit her aging \
father, Atticus. Set against the backdrop of the civil rights tensions.",
              author="Harper Lee",
              price="$16.62",
              book_genre=book_genre3)
session.add(book4)
session.commit()

book5 = Books(user_id=1,name="Gone Girl",
              description="Marriage can be a real killer. One of the most critically acclaimed suspense writers of our \
time, New York Times bestseller Gillian Flynn takes that statement to its darkest place in this unputdownable masterpiece \
about a marriage gone terribly, terribly wrong",
              author="Gillian Flynn",
              price="$16.38",
              book_genre=book_genre3)
session.add(book5)
session.commit()

# List for Genre 4
book_genre4 = Book_genres(user_id=1,name="Mystery & Crime")

session.add(book_genre4)
session.commit()

book1 = Books(user_id=1,name="The Girl on the Train",
              description="A debut psychological thriller that will forever change the way you look at other people's lives.",
              author="Paula Hawkins",
              price="$16.23",
              book_genre=book_genre4)

session.add(book1)
session.commit()


book2 = Books(user_id=1,name="The Cuckoo's Calling",
              description="A brilliant debut mystery in a classic vein: Detective Cormoran Strike investigates a supermodel's suicide.", 
              author="Robert Galbraith, J. K. Rowling",
              price="$11.45",
              book_genre=book_genre4)
session.add(book2)
session.commit()

book3 = Books(user_id=1,name="Inferno",
              description="Harvard professor of symbology Robert Langdon awakens in an \
Italian hospital, disoriented and with no recollection of the past thirty-six hours, including the origin of the macabre \
object hidden in his belongings. With a relentless female assassin trailing them through Florence, he and his resourceful \
doctor, Sienna Brooks, are forced to flee",
              author="Dan Brown",
              price="$12.80",
              book_genre=book_genre4)

session.add(book3)
session.commit()

book4 = Books(user_id=1,name="The complete works of Sherlock Holmes",
              description="A master of deductive reasoning who can solve the most \
difficult crimes by spotting obscure clues overlooked by others, dilettante sleuth Sherlock Holmes was the hero of sixty stories \
written by Sir Arthur Conan Doyle between 1887 and 1927. With the help of his loyal friend, Doctor Watson, Holmes brought \
countless crooks, thieves, swindlers, and murderers to justice. He even rose from the dead after Doyle tried to dispatch him\
in his twenty-fourth adventure, and readers protested. Some Sherlock Holmes stories rank among the most famous in detective \
fiction, among them - A Study in Scarlet, A Scandal in Bohemia, The Speckled Band, and The Hound of the Baskervilles.",
              author="Arthur Conan Doyle",
              price="$18.00",
              book_genre=book_genre4)
session.add(book4)
session.commit()

book5 = Books(user_id=1,name="Dark Places",
              description="Libby Day was seven when her mother and two sisters were murdered in - \
The Satan Sacrifice of Kinnakee, Kansas. She survived and famously testified that her fifteen-year-old brother, \
Ben, was the killer. Twenty-five years later, the Kill Club, a secret society obsessed with notorious crimes locates \
Libby and pumps her for details.",
              author="Gillian Flynn",
              price="$8.45",
              book_genre=book_genre4)
session.add(book5)
session.commit()

# List for Genre 5
book_genre5 = Book_genres(user_id=1,name="Romance")

session.add(book_genre5)
session.commit()

book1 = Books(user_id=1,name="Stars of Fortune",
              description="To celebrate the rise of their new queen, three goddesses of the \
moon created three stars, one of fire, one of ice, one of water. But then they fell from the sky, putting the fate of all worlds \
in danger. And now three women and three men join forces to pick up the pieces",
              author="Nora Roberts",
              price="$10.20",
              book_genre=book_genre5)

session.add(book1)
session.commit()


book2 = Books(user_id=1,name="Undercover",
              description="Marshall Everett has traveled a twisting, perilous road from the jungles of \
South America to the streets of Paris. As an undercover DEA agent, Marshall penetrated a powerful cartel and became the trusted \
right-hand man of a ruthless drug lord. ",
              author="Danielle Steel",
              price="$17.97",
              book_genre=book_genre5) 
session.add(book2)
session.commit()

book3 = Books(user_id=1,name="The Choice",
              description="Travis Parker has everything a man could want: a good job, loyal friends, even a \
waterfront home in small-town North Carolina. In full pursuit of the good life-- boating, swimming, and regular barbecues with \
his good-natured buddies--he holds the vague conviction that a serious relationship with a woman would only cramp his style.\
That is, until Gabby Holland moves in next door. ",
              author="Nicholas Sparks",
              price="$7.99",
              book_genre=book_genre5)

session.add(book3)
session.commit()
print "added book genres!"
