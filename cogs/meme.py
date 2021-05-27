import requests
import random
import discord

from discord.ext import commands
from io import BytesIO
from PIL import Image
from etc.error_handling import invalid_argument


class Meme(commands.Cog):
    def __init__(self, bot):
        self.available_memes = ['10-Guy', '1950s-Middle-Finger', '1990s-First-World-Problems',
                                '1st-World-Canadian-Problems', '2nd-Term-Obama', 'Aaaaand-Its-Gone', 'Ace-Primo',
                                'Actual-Advice-Mallard', 'Adalia-Rose', 'Admiral-Ackbar-Relationship-Expert',
                                'Advice-Dog', 'Advice-Doge', 'Advice-God', 'Advice-Peeta', 'Advice-Tam', 'Advice-Yoda',
                                'Afraid-To-Ask-Andy', 'Afraid-To-Ask-Andy-Closeup', 'Aint-Nobody-Got-Time-For-That',
                                'Alan-Greenspan', 'Alarm-Clock', 'Albert-Cagestein', 'Albert-Einstein-1',
                                'Alien-Meeting-Suggestion', 'Alright-Gentlemen-We-Need-A-New-Idea', 'Always-Has-Been',
                                'Alyssa-Silent-Hill', 'Am-I-The-Only-One-Around-Here', 'American-Chopper-Argument',
                                'Ancient-Aliens', 'And-everybody-loses-their-minds', 'And-then-I-said-Obama',
                                'Angry-Asian', 'Angry-Baby', 'Angry-Birds-Pig', 'Angry-Bride',
                                'Angry-Chef-Gordon-Ramsay', 'Angry-Chicken-Boss', 'Angry-Dumbledore', 'Angry-Koala',
                                'Angry-Rant-Randy', 'Angry-Toddler', 'Annoying-Childhood-Friend',
                                'Annoying-Facebook-Girl', 'Anri-Stares', 'Anti-Joke-Chicken', 'Apathetic-Xbox-Laser',
                                'Archer', 'Are-Your-Parents-Brother-And-Sister', 'Are-you-a-Wizard',
                                'Arrogant-Rich-Man',
                                'Art-Attack', 'Art-Student-Owl', 'Arthur-Fist', 'Asshole-Ref', 'Aunt-Carol',
                                'Austin-Powers-Honestly', 'Aw-Yeah-Rage-Face', 'Awkward-Moment-Sealion',
                                'Awkward-Olympics', 'BANE-AND-BRUCE', 'BM-Employees', 'Babushkas-On-Facebook',
                                'Baby-Cry', 'Baby-Godfather', 'Baby-Insanity-Wolf', 'Back-In-My-Day', 'Bad-Advice-Cat',
                                'Bad-Joke-Eel', 'Bad-Luck-Bear', 'Bad-Luck-Brian', 'Bad-Luck-Hannah',
                                'Bad-Pun-Anna-Kendrick', 'Bad-Pun-Dog', 'Bad-Wife-Worse-Mom', 'Bah-Humbug', 'Bane',
                                'Bane-Permission', 'Barack-And-Kumar-2013', 'Barba', 'Barbosa-And-Sparrow',
                                'Barney-Stinson-Win', 'Baromney', 'Baron-Creater', 'Bart-Simpson-Peeking',
                                'Batman-And-Superman', 'Batman-Slapping-Robin', 'Batman-Smiles', 'Batmobile',
                                'Bazooka-Squirrel', 'Be-Like-Bill', 'Bear-Grylls', 'Beard-Baby', 'Bebo',
                                'Because-Race-Car', 'Ben-Barba-Pointing', 'Bender', 'Benito',
                                'Bernie-I-Am-Once-Again-Asking-For-Your-Support', 'Beyonce-Knowles-Superbowl',
                                'Beyonce-Knowles-Superbowl-Face', 'Beyonce-Superbowl-Yell', 'Big-Bird',
                                'Big-Bird-And-Mitt-Romney', 'Big-Bird-And-Snuffy', 'Big-Ego-Man', 'Big-Family-Comeback',
                                'Bike-Fall', 'Bill-Murray-Golf', 'Bill-Nye-The-Science-Guy', 'Bill-OReilly',
                                'Billy-Graham-Mitt-Romney', 'Bitch-Please', 'Black-Girl-Wat', 'Blank-Blue-Background',
                                'Blank-Colored-Background', 'Blank-Comic-Panel-1x2', 'Blank-Comic-Panel-2x1',
                                'Blank-Comic-Panel-2x2', 'Blank-Nut-Button', 'Blank-Starter-Pack',
                                'Blank-Transparent-Square', 'Blank-Yellow-Sign', 'Blob', 'Blue-Futurama-Fry',
                                'Boardroom-Meeting-Suggestion', 'Bonobo-Lyfe', 'Booty-Warrior', 'Bothered-Bond',
                                'Brace-Yourselves-X-is-Coming', 'Brian-Burke-On-The-Phone', 'Brian-Griffin',
                                'Brian-Williams-Was-There', 'Brian-Williams-Was-There-2', 'Brian-Williams-Was-There-3',
                                'Brian-Wilson-Vs-ZZ-Top',
                                'Britney-Spears', 'Bubba-And-Barack', 'Buddy-Christ', 'Buddy-The-Elf',
                                'Buff-Doge-vs-Cheems', 'Bullets', 'Burn-Kitty', 'Business-Cat',
                                'But-Thats-None-Of-My-Business', 'But-Thats-None-Of-My-Business-Neutral',
                                'Butthurt-Dweller', 'CASHWAG-Crew', 'CURLEY', 'Captain-Hindsight',
                                'Captain-Phillips-Im-The-Captain-Now', 'Captain-Picard-Facepalm',
                                'Car-Salesman-Slaps-Hood', 'Casper', 'Castaway-Fire', 'Ceiling-Cat', 'Cel-Jesuno',
                                'Cereal-Guy', 'Cereal-Guy-Spitting', 'Cereal-Guys-Daddy', 'Chad-Johnson',
                                'Chainsaw-Bear', 'Challenge-Accepted-Rage-Face', 'Change-My-Mind', 'Charlie-Sheen-Derp',
                                'Chavez', 'Chef-Gordon-Ramsay', 'Chemistry-Cat', 'Chester-The-Cat', 'Chicken-Bob',
                                'Chief-Keef', 'Chihuahua-dog', 'Chill-Out-Lemur', 'Chinese-Cat', 'Chocolate-Spongebob',
                                'Chubby-Bubbles-Girl', 'Chuck-Norris', 'Chuck-Norris-Approves', 'Chuck-Norris-Finger',
                                'Chuck-Norris-Flex', 'Chuck-Norris-Guns', 'Chuck-Norris-Laughing', 'Chuck-Norris-Phone',
                                'Chuck-Norris-With-Guns', 'Chuckchuckchuck', 'City-Bear', 'Cleavage-Girl', 'Clefable',
                                'Close-Enough', 'Clown-Applying-Makeup', 'College-Freshman', 'College-Liberal',
                                'Comic-Book-Guy', 'Computer-Guy', 'Computer-Guy-Facepalm', 'Computer-Horse',
                                'Condescending-Goku', 'Condescending-Wonka', 'Confession-Bear', 'Confused-Cam',
                                'Confused-Gandalf', 'Confused-Granddad', 'Confused-Lebowski', 'Confused-Mel-Gibson',
                                'Conspiracy-Keanu', 'Consuela', 'Contradictory-Chris', 'Cool-Cat-Stroll', 'Cool-Obama',
                                'Cool-Story-Bro', 'Corona', 'Costanza', 'Coulson', 'Courage-Wolf', 'Crazy-Dawg',
                                'Crazy-Girlfriend-Praying-Mantis', 'Crazy-Hispanic-Man', 'Creeper-Dog',
                                'Creepy-Condescending-Wonka', 'Criana', 'Crosseyed-Goku', 'Crying-Because-Of-Cute',
                                'Cute-Cat', 'Cute-Dog', 'Cute-Puppies', 'DJ-Pauly-D', 'Dad-Joke-Dog',
                                'Dafuq-Did-I-Just-Read', 'Dallas-Cowboys', 'Dancing-Trollmom', 'Darth-Maul',
                                'Darti-Boy',
                                'Dat-Ass', 'Dat-Boi', 'Dating-Site-Murderer', 'Dave-Chappelle', 'Dead-Space',
                                'Deadpool-Pick-Up-Lines', 'Deadpool-Surprised', 'Depressed-Cat', 'Depression-Dog',
                                'Derp', 'Derpina', 'Determined-Guy-Rage-Face', 'Dexter', 'Dick-Cheney',
                                'Disappointed-Tyson', 'Disaster-Girl', 'Distracted-Boyfriend', 'Do-I-Care-Doe', 'Doge',
                                'Doge-2', 'Dolph-Ziggler-Sells', 'Donald-Trump-sewing-his-name-into-the-American-Flag',
                                'Dont-You-Squidward', 'DoucheBag-DJ', 'Doug', 'Down-Syndrome', 'Downcast-Dark-Souls',
                                'Downvoting-Roman', 'Dr-Crane', 'Dr-Evil', 'Dr-Evil-Laser', 'Drake-Bad-Good',
                                'Drake-Hotline-Bling', 'Drunk-Baby', 'Duck-Face', 'Duck-Face-Chicks', 'Dumb-Blonde',
                                'Dwight-Schrute', 'Dwight-Schrute-2', 'ERMAHGERD-TWERLERT', 'Edu-Camargo',
                                'Edward-Elric-1', 'Efrain-Juarez', 'Eighties-Teen', 'Eminem', 'Empty-Red-And-Black',
                                'Endel-Tulviste', 'Engineering-Professor', 'Epic-Handshake', 'Epicurist-Kid',
                                'Ermahgerd-Berks', 'Ermahgerd-Beyonce', 'Ermahgerd-IPHERN-3GM', 'Error-404',
                                'Evil-Baby',
                                'Evil-Cows', 'Evil-Kermit', 'Evil-Otter', 'Evil-Plotting-Raccoon', 'Evil-Toddler',
                                'Excited-Cat', 'Excited-Minions', 'Expanding-Brain', 'Eye-Of-Sauron',
                                'FFFFFFFUUUUUUUUUUUU', 'FRANGO', 'Fabulous-Frank-And-His-Snake',
                                'Face-You-Make-Robert-Downey-Jr', 'Facepalm-Bear', 'Fake-Hurricane-Guy',
                                'Family-Guy-Brian', 'Family-Guy-Peter', 'Family-Tech-Support-Guy',
                                'Fast-Furious-Johnny-Tran', 'Fat-Cat', 'Fat-Val-Kilmer', 'Father-Ted',
                                'Fear-And-Loathing-Cat', 'Feels-Bad-Frog---Feels-Bad-Man', 'Felix-Baumgartner',
                                'Felix-Baumgartner-Lulz', 'Fernando-Litre', 'Fifa-E-Call-Of-Duty', 'Fim-De-Semana',
                                'Finding-Neverland', 'Fini', 'Finn-The-Human', 'First-Day-On-The-Internet-Kid',
                                'First-World-Frat-Guy', 'First-World-Problems', 'First-World-Problems-Cat',
                                'First-World-Stoner-Problems', 'Fk-Yeah', 'Flavor-Flav', 'Foal-Of-Mine',
                                'Folean-Dynamite', 'Forever-Alone', 'Forever-Alone-Christmas', 'Forever-Alone-Happy',
                                'Foul-Bachelor-Frog', 'Foul-Bachelorette-Frog', 'Friend-Zone-Fiona',
                                'Frowning-Nun', 'Frustrated-Boromir', 'Frustrating-Mom', 'Futurama-Fry',
                                'Futurama-Leela', 'Futurama-Zoidberg', 'Gaga-Baby', 'Gandhi', 'Gangnam-Style',
                                'Gangnam-Style-PSY', 'Gangnam-Style2', 'Gangster-Baby', 'Gasp-Rage-Face', 'George-Bush',
                                'George-Washington', 'Ghetto-Jesus', 'Ghost-Nappa', 'Giovanni-Vernia',
                                'Give-me-Karma---Beating-the-dead-horse', 'Gladys-Falcon', 'God', 'Gollum',
                                'Good-Fellas-Hilarious', 'Good-Guy-Greg', 'Good-Guy-Pizza-Rolls', 'Good-Guy-Putin',
                                'Good-Guy-Socially-Awkward-Penguin', 'Google-Chrome', 'Gordo', 'Got-Room-For-One-More',
                                'Gotta-Go-Cat', 'Grandma-Finds-The-Internet', 'Green-Day', 'Grumpy-Cat',
                                'Grumpy-Cat-Bed', 'Grumpy-Cat-Birthday', 'Grumpy-Cat-Christmas',
                                'Grumpy-Cat-Does-Not-Believe', 'Grumpy-Cat-Halloween', 'Grumpy-Cat-Happy',
                                'Grumpy-Cat-Mistletoe', 'Grumpy-Cat-Not-Amused', 'Grumpy-Cat-Reverse', 'Grumpy-Cat-Sky',
                                'Grumpy-Cat-Star-Wars', 'Grumpy-Cat-Table', 'Grumpy-Cat-Top-Hat', 'Grumpy-Cats-Father',
                                'Grumpy-Toad', 'Grus-Plan', 'Guinness-World-Record', 'Guy-Fawkes',
                                'Guy-Holding-Cardboard-Sign', 'Hal-Jordan', 'Hamtaro', 'Han-Solo',
                                'Happy-Guy-Rage-Face',
                                'Happy-Minaj', 'Happy-Minaj-2', 'Happy-Star-Congratulations', 'Hard-To-Swallow-Pills',
                                'Hardworking-Guy', 'Harley-Quinn', 'Harmless-Scout-Leader', 'Harper-WEF',
                                'Harry-Potter-Ok', 'Hawkward', 'He-Needs-The-Vaccine', 'He-Will-Never-Get-A-Girlfriend',
                                'Headbanzer', 'Headless-Rider-DRRR', 'Heavy-Breathing-Cat', 'Hedonism-Bot',
                                'Hello-Kassem', 'Hello-Kitty', 'Helpful-Tyler-Durden', 'Henry-David-Thoreau',
                                'Hercules-Hades', 'Heres-Johnny', 'Herm-Edwards', 'Hey-Internet',
                                'Hide-Yo-Kids-Hide-Yo-Wife', 'Hide-the-Pain-Harold', 'High-Dog',
                                'High-Expectations-Asian-Father', 'Hillary-Clinton', 'Hillary-Clinton-Cellphone',
                                'Hipster-Ariel', 'Hipster-Barista', 'Hipster-Kitty', 'Hohoho', 'Homophobic-Seal',
                                'Hoody-Cat', 'Hora-Extra', 'Hornist-Hamster', 'Horny-Harry', 'Hot-Caleb', 'Hot-Scale',
                                'Hotline-Miami-Richard', 'House-Bunny', 'How-About-No-Bear', 'How-Tough-Are-You',
                                'Hypnotoad', 'Hypocritical-Islam-Terrorist', 'Hysterical-Tom',
                                'I-Am-Not-A-Gator-Im-A-X',
                                'I-Bet-Hes-Thinking-About-Other-Women', 'I-Forsee', 'I-Guarantee-It',
                                'I-Have-No-Idea-What-I-Am-Doing', 'I-Have-No-Idea-What-I-Am-Doing-Dog',
                                'I-Know-Fuck-Me-Right', 'I-Know-That-Feel-Bro', 'I-Lied-2', 'I-See-Dead-People',
                                'I-Should-Buy-A-Boat-Cat', 'I-Too-Like-To-Live-Dangerously',
                                'I-Was-Told-There-Would-Be',
                                'I-Will-Find-You-And-Kill-You', 'Idiot-Nerd-Girl', 'Idiotaco',
                                'If-You-Know-What-I-Mean-Bean', 'Ill-Have-You-Know-Spongebob', 'Ill-Just-Wait-Here',
                                'Im-Curious-Nappa', 'Im-Fabulous-Adam', 'Im-The-Captain-Now', 'Imagination-Spongebob',
                                'Impossibru-Guy-Original', 'Inception', 'Inhaling-Seagull', 'Inigo-Montoya',
                                'Innocent-Sasha', 'Insanity-Puppy', 'Insanity-Wolf', 'Intelligent-Dog',
                                'Internet-Explorer', 'Internet-Guide', 'Interupting-Kanye', 'Invalid-Argument-Vader',
                                'Is-This-A-Pigeon', 'Islam-Rage---Angry-Muslim', 'Its-Finally-Over',
                                'Its-Not-Going-To-Happen', 'Its-True-All-of-It-Han-Solo',
                                'Jack-Nicholson-The-Shining-Snow', 'Jack-Sparrow-Being-Chased', 'Jackie-Chan-WTF',
                                'Jammin-Baby', 'Jay-Knows-Facts', 'Jehovas-Witness-Squirrel', 'Jerkoff-Javert',
                                'Jersey-Santa', 'Jessica-Nigri-Cosplay', 'Jesus-Talking-To-Cool-Dude',
                                'Jim-Lehrer-The-Man', 'Joe-Biden', 'John-Riley-Condescension', 'Joker',
                                'Joker-Rainbow-Hands', 'Jon-Stewart-Skeptical', 'Joo-Espontneo', 'Joseph-Ducreux',
                                'Justin-Bieber-Suit', 'Karate-Kid', 'Karate-Kyle', 'Keep']

        self.available_memes_pretty = ['10 Guy', '1950s Middle Finger', '1990s First World Problems',
                                       '1st World Canadian Problems', '2nd Term Obama', 'Aaaaand Its Gone', 'Ace Primo',
                                       'Actual Advice Mallard', 'Adalia Rose', 'Admiral Ackbar Relationship Expert',
                                       'Advice Dog', 'Advice Doge', 'Advice God', 'Advice Peeta', 'Advice Tam',
                                       'Advice Yoda', 'Afraid To Ask Andy', 'Afraid To Ask Andy Closeup',
                                       'Aint Nobody Got Time For That', 'Alan Greenspan', 'Alarm Clock',
                                       'Albert Cagestein', 'Albert Einstein 1', 'Alien Meeting Suggestion',
                                       'Alright Gentlemen We Need A New Idea', 'Always Has Been', 'Alyssa Silent Hill',
                                       'Am I The Only One Around Here', 'American Chopper Argument', 'Ancient Aliens',
                                       'And everybody loses their minds', 'And then I said Obama', 'Angry Asian',
                                       'Angry Baby', 'Angry Birds Pig', 'Angry Bride', 'Angry Chef Gordon Ramsay',
                                       'Angry Chicken Boss', 'Angry Dumbledore', 'Angry Koala', 'Angry Rant Randy',
                                       'Angry Toddler', 'Annoying Childhood Friend', 'Annoying Facebook Girl',
                                       'Anri Stares', 'Anti Joke Chicken', 'Apathetic Xbox Laser', 'Archer',
                                       'Are Your Parents Brother And Sister', 'Are you a Wizard', 'Arrogant Rich Man',
                                       'Art Attack', 'Art Student Owl', 'Arthur Fist', 'Asshole Ref', 'Aunt Carol',
                                       'Austin Powers Honestly', 'Aw Yeah Rage Face', 'Awkward Moment Sealion',
                                       'Awkward Olympics', 'BANE AND BRUCE', 'BM Employees', 'Babushkas On Facebook',
                                       'Baby Cry', 'Baby Godfather', 'Baby Insanity Wolf', 'Back In My Day',
                                       'Bad Advice Cat', 'Bad Joke Eel', 'Bad Luck Bear', 'Bad Luck Brian',
                                       'Bad Luck Hannah', 'Bad Pun Anna Kendrick', 'Bad Pun Dog', 'Bad Wife Worse Mom',
                                       'Bah Humbug', 'Bane', 'Bane Permission', 'Barack And Kumar 2013', 'Barba',
                                       'Barbosa And Sparrow', 'Barney Stinson Win', 'Baromney', 'Baron Creater',
                                       'Bart Simpson Peeking', 'Batman And Superman', 'Batman Slapping Robin',
                                       'Batman Smiles', 'Batmobile', 'Bazooka Squirrel', 'Be Like Bill', 'Bear Grylls',
                                       'Beard Baby', 'Bebo', 'Because Race Car', 'Ben Barba Pointing', 'Bender',
                                       'Benito', 'Bernie I Am Once Again Asking For Your Support',
                                       'Beyonce Knowles Superbowl', 'Beyonce Knowles Superbowl Face',
                                       'Beyonce Superbowl Yell', 'Big Bird', 'Big Bird And Mitt Romney',
                                       'Big Bird And Snuffy', 'Big Ego Man', 'Big Family Comeback', 'Bike Fall',
                                       'Bill Murray Golf', 'Bill Nye The Science Guy', 'Bill OReilly',
                                       'Billy Graham Mitt Romney', 'Bitch Please', 'Black Girl Wat',
                                       'Blank Blue Background', 'Blank Colored Background', 'Blank Comic Panel 1x2',
                                       'Blank Comic Panel 2x1', 'Blank Comic Panel 2x2', 'Blank Nut Button',
                                       'Blank Starter Pack', 'Blank Transparent Square', 'Blank Yellow Sign', 'Blob',
                                       'Blue Futurama Fry', 'Boardroom Meeting Suggestion', 'Bonobo Lyfe',
                                       'Booty Warrior', 'Bothered Bond', 'Brace Yourselves X is Coming',
                                       'Brian Burke On The Phone', 'Brian Griffin', 'Brian Williams Was There',
                                       'Brian Williams Was There 2', 'Brian Williams Was There 3',
                                       'Brian Wilson Vs ZZ Top', 'Britney Spears', 'Bubba And Barack', 'Buddy Christ',
                                       'Buddy The Elf', 'Buff Doge vs Cheems', 'Bullets', 'Burn Kitty', 'Business Cat',
                                       'But Thats None Of My Business', 'But Thats None Of My Business Neutral',
                                       'Butthurt Dweller', 'CASHWAG Crew', 'CURLEY', 'Captain Hindsight',
                                       'Captain Phillips Im The Captain Now', 'Captain Picard Facepalm',
                                       'Car Salesman Slaps Hood', 'Casper', 'Castaway Fire', 'Ceiling Cat',
                                       'Cel Jesuno',
                                       'Cereal Guy', 'Cereal Guy Spitting', 'Cereal Guys Daddy', 'Chad Johnson',
                                       'Chainsaw Bear', 'Challenge Accepted Rage Face', 'Change My Mind',
                                       'Charlie Sheen Derp', 'Chavez', 'Chef Gordon Ramsay', 'Chemistry Cat',
                                       'Chester The Cat', 'Chicken Bob', 'Chief Keef', 'Chihuahua dog',
                                       'Chill Out Lemur', 'Chinese Cat', 'Chocolate Spongebob', 'Chubby Bubbles Girl',
                                       'Chuck Norris', 'Chuck Norris Approves', 'Chuck Norris Finger',
                                       'Chuck Norris Flex', 'Chuck Norris Guns', 'Chuck Norris Laughing',
                                       'Chuck Norris Phone', 'Chuck Norris With Guns', 'Chuckchuckchuck', 'City Bear',
                                       'Cleavage Girl', 'Clefable', 'Close Enough', 'Clown Applying Makeup',
                                       'College Freshman', 'College Liberal', 'Comic Book Guy', 'Computer Guy',
                                       'Computer Guy Facepalm', 'Computer Horse', 'Condescending Goku',
                                       'Condescending Wonka', 'Confession Bear', 'Confused Cam', 'Confused Gandalf',
                                       'Confused Granddad', 'Confused Lebowski', 'Confused Mel Gibson',
                                       'Conspiracy Keanu', 'Consuela', 'Contradictory Chris', 'Cool Cat Stroll',
                                       'Cool Obama', 'Cool Story Bro', 'Corona', 'Costanza', 'Coulson', 'Courage Wolf',
                                       'Crazy Dawg', 'Crazy Girlfriend Praying Mantis', 'Crazy Hispanic Man',
                                       'Creeper Dog', 'Creepy Condescending Wonka', 'Criana', 'Crosseyed Goku',
                                       'Crying Because Of Cute', 'Cute Cat', 'Cute Dog', 'Cute Puppies', 'DJ Pauly D',
                                       'Dad Joke Dog', 'Dafuq Did I Just Read', 'Dallas Cowboys', 'Dancing Trollmom',
                                       'Darth Maul', 'Darti Boy', 'Dat Ass', 'Dat Boi', 'Dating Site Murderer',
                                       'Dave Chappelle', 'Dead Space', 'Deadpool Pick Up Lines', 'Deadpool Surprised',
                                       'Depressed Cat', 'Depression Dog', 'Derp', 'Derpina', 'Determined Guy Rage Face',
                                       'Dexter', 'Dick Cheney', 'Disappointed Tyson', 'Disaster Girl',
                                       'Distracted Boyfriend', 'Do I Care Doe', 'Doge', 'Doge 2', 'Dolph Ziggler Sells',
                                       'Donald Trump sewing his name into the American Flag', 'Dont You Squidward',
                                       'DoucheBag DJ', 'Doug', 'Down Syndrome', 'Downcast Dark Souls',
                                       'Downvoting Roman', 'Dr Crane', 'Dr Evil', 'Dr Evil Laser', 'Drake Bad Good',
                                       'Drake Hotline Bling', 'Drunk Baby', 'Duck Face', 'Duck Face Chicks',
                                       'Dumb Blonde', 'Dwight Schrute', 'Dwight Schrute 2', 'ERMAHGERD TWERLERT',
                                       'Edu Camargo', 'Edward Elric 1', 'Efrain Juarez', 'Eighties Teen', 'Eminem',
                                       'Empty Red And Black', 'Endel Tulviste', 'Engineering Professor',
                                       'Epic Handshake', 'Epicurist Kid', 'Ermahgerd Berks', 'Ermahgerd Beyonce',
                                       'Ermahgerd IPHERN 3GM', 'Error 404', 'Evil Baby', 'Evil Cows', 'Evil Kermit',
                                       'Evil Otter', 'Evil Plotting Raccoon', 'Evil Toddler', 'Excited Cat',
                                       'Excited Minions', 'Expanding Brain', 'Eye Of Sauron', 'FFFFFFFUUUUUUUUUUUU',
                                       'FRANGO', 'Fabulous Frank And His Snake', 'Face You Make Robert Downey Jr',
                                       'Facepalm Bear', 'Fake Hurricane Guy', 'Family Guy Brian', 'Family Guy Peter',
                                       'Family Tech Support Guy', 'Fast Furious Johnny Tran', 'Fat Cat',
                                       'Fat Val Kilmer', 'Father Ted', 'Fear And Loathing Cat',
                                       'Feels Bad Frog   Feels Bad Man', 'Felix Baumgartner', 'Felix Baumgartner Lulz',
                                       'Fernando Litre', 'Fifa E Call Of Duty', 'Fim De Semana', 'Finding Neverland',
                                       'Fini', 'Finn The Human', 'First Day On The Internet Kid',
                                       'First World Frat Guy',
                                       'First World Problems', 'First World Problems Cat',
                                       'First World Stoner Problems',
                                       'Fk Yeah', 'Flavor Flav', 'Foal Of Mine', 'Folean Dynamite', 'Forever Alone',
                                       'Forever Alone Christmas', 'Forever Alone Happy', 'Foul Bachelor Frog',
                                       'Foul Bachelorette Frog', 'Friend Zone Fiona', 'Frowning Nun',
                                       'Frustrated Boromir', 'Frustrating Mom', 'Futurama Fry', 'Futurama Leela',
                                       'Futurama Zoidberg', 'Gaga Baby', 'Gandhi', 'Gangnam Style', 'Gangnam Style PSY',
                                       'Gangnam Style2', 'Gangster Baby', 'Gasp Rage Face', 'George Bush',
                                       'George Washington', 'Ghetto Jesus', 'Ghost Nappa', 'Giovanni Vernia',
                                       'Give me Karma   Beating the dead horse', 'Gladys Falcon', 'God', 'Gollum',
                                       'Good Fellas Hilarious', 'Good Guy Greg', 'Good Guy Pizza Rolls',
                                       'Good Guy Putin', 'Good Guy Socially Awkward Penguin', 'Google Chrome', 'Gordo',
                                       'Got Room For One More', 'Gotta Go Cat', 'Grandma Finds The Internet',
                                       'Green Day', 'Grumpy Cat', 'Grumpy Cat Bed', 'Grumpy Cat Birthday',
                                       'Grumpy Cat Christmas', 'Grumpy Cat Does Not Believe', 'Grumpy Cat Halloween',
                                       'Grumpy Cat Happy', 'Grumpy Cat Mistletoe', 'Grumpy Cat Not Amused',
                                       'Grumpy Cat Reverse', 'Grumpy Cat Sky', 'Grumpy Cat Star Wars',
                                       'Grumpy Cat Table', 'Grumpy Cat Top Hat', 'Grumpy Cats Father', 'Grumpy Toad',
                                       'Grus Plan', 'Guinness World Record', 'Guy Fawkes', 'Guy Holding Cardboard Sign',
                                       'Hal Jordan', 'Hamtaro', 'Han Solo', 'Happy Guy Rage Face', 'Happy Minaj',
                                       'Happy Minaj 2', 'Happy Star Congratulations', 'Hard To Swallow Pills',
                                       'Hardworking Guy', 'Harley Quinn', 'Harmless Scout Leader', 'Harper WEF',
                                       'Harry Potter Ok', 'Hawkward', 'He Needs The Vaccine',
                                       'He Will Never Get A Girlfriend', 'Headbanzer', 'Headless Rider DRRR',
                                       'Heavy Breathing Cat', 'Hedonism Bot', 'Hello Kassem', 'Hello Kitty',
                                       'Helpful Tyler Durden', 'Henry David Thoreau', 'Hercules Hades', 'Heres Johnny',
                                       'Herm Edwards', 'Hey Internet', 'Hide Yo Kids Hide Yo Wife',
                                       'Hide the Pain Harold', 'High Dog', 'High Expectations Asian Father',
                                       'Hillary Clinton', 'Hillary Clinton Cellphone', 'Hipster Ariel',
                                       'Hipster Barista', 'Hipster Kitty', 'Hohoho', 'Homophobic Seal', 'Hoody Cat',
                                       'Hora Extra', 'Hornist Hamster', 'Horny Harry', 'Hot Caleb', 'Hot Scale',
                                       'Hotline Miami Richard', 'House Bunny', 'How About No Bear', 'How Tough Are You',
                                       'Hypnotoad', 'Hypocritical Islam Terrorist', 'Hysterical Tom',
                                       'I Am Not A Gator Im A X', 'I Bet Hes Thinking About Other Women', 'I Forsee',
                                       'I Guarantee It', 'I Have No Idea What I Am Doing',
                                       'I Have No Idea What I Am Doing Dog', 'I Know Fuck Me Right',
                                       'I Know That Feel Bro', 'I Lied 2', 'I See Dead People',
                                       'I Should Buy A Boat Cat', 'I Too Like To Live Dangerously',
                                       'I Was Told There Would Be', 'I Will Find You And Kill You', 'Idiot Nerd Girl',
                                       'Idiotaco', 'If You Know What I Mean Bean', 'Ill Have You Know Spongebob',
                                       'Ill Just Wait Here', 'Im Curious Nappa', 'Im Fabulous Adam',
                                       'Im The Captain Now', 'Imagination Spongebob', 'Impossibru Guy Original',
                                       'Inception', 'Inhaling Seagull', 'Inigo Montoya', 'Innocent Sasha',
                                       'Insanity Puppy', 'Insanity Wolf', 'Intelligent Dog', 'Internet Explorer',
                                       'Internet Guide', 'Interupting Kanye', 'Invalid Argument Vader',
                                       'Is This A Pigeon', 'Islam Rage   Angry Muslim', 'Its Finally Over',
                                       'Its Not Going To Happen', 'Its True All of It Han Solo',
                                       'Jack Nicholson The Shining Snow', 'Jack Sparrow Being Chased',
                                       'Jackie Chan WTF',
                                       'Jammin Baby', 'Jay Knows Facts', 'Jehovas Witness Squirrel', 'Jerkoff Javert',
                                       'Jersey Santa', 'Jessica Nigri Cosplay', 'Jesus Talking To Cool Dude',
                                       'Jim Lehrer The Man', 'Joe Biden', 'John Riley Condescension', 'Joker',
                                       'Joker Rainbow Hands', 'Jon Stewart Skeptical', 'Joo Espontneo',
                                       'Joseph Ducreux',
                                       'Justin Bieber Suit', 'Karate Kid', 'Karate Kyle', 'Keep']
        self.bot = bot
        self.old_memes = {}

    @commands.command()
    async def meme(self, ctx, *args):
        try:
            await ctx.send(requests.get("https://meme-api.herokuapp.com/gimme").json()["url"])
        except:
            await ctx.send("Die Meme API ist aktuell nicht verfügbar.")

    @commands.command()
    async def gen_meme(self, ctx, *args):
        if args:
            try:
                member = [ctx.guild.get_member(int(str(x).strip("<>!@"))) for x in args][0]

                if member:
                    try:
                        string = self.old_memes[str(member)]
                    except:
                        return await ctx.send(f"Es wurde leider kein altes Meme von {str(member)} gefunden.")

                else:
                    string = str(ctx.message.author)

            except:
                string = " ".join(args)

            self.old_memes[str(ctx.message.author)] = string

        else:
            try:
                string = self.old_memes[str(ctx.message.author)]

            except:
                return await invalid_argument(self, ctx, command="gen_meme")

        meme = random.choice(self.available_memes)

        try:
            top_text = string[:string.index(",")]
        except:
            try:
                top_text = string[:string.index(";")]
            except:
                top_text = ' '.join(args)

        if "," in string:
            bottom_text = string[string.index(",") + 1:]
        elif ";" in string:
            bottom_text = string[string.index(";") + 1:]
        else:
            bottom_text = " "

        url = f"http://apimeme.com/meme?meme={meme}&top={top_text}&bottom={bottom_text}"
        img = Image.open(BytesIO(requests.get(url).content))

        with BytesIO() as output:
            img.save(output, format="PNG")
            output.seek(0)
            try:
                meme = await ctx.send(file=discord.File(fp=output, filename=ctx.message.content + ".png"),
                                      content=f"by: {member.mention}, mentioned by: {ctx.message.author.mention}")
            except:
                meme = await ctx.send(file=discord.File(fp=output, filename=ctx.message.content + ".png"),
                                      content=f"by: {ctx.message.author.mention}")


def setup(bot):
    bot.add_cog(Meme(bot))
