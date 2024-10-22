import time
import random
from pynostr.event import Event
from pynostr.relay_manager import RelayManager
from pynostr.key import PrivateKey
import datetime

# Replace with your private key
NOSTR_PRIVATE_KEY = "YourNsecHere"

# Define the relays to publish into
NOSTR_RELAYS = [
    "wss://relay.damus.io",
    "wss://nostr.bitcoiner.social",
    "wss://nostr.oxtr.dev",
    "wss://nostr.fmt.wiz.biz",
    "wss://relay.nostr.info",
    "wss://relay.nostr.bg",
    "wss://nostr.onsats.org",
    "wss://nostr-pub.wellorder.net",
    "wss://relay.snort.social",
    "wss://relay.current.fyi",
    "wss://nostr.orangepill.dev",
    "wss://relay.nostrgraph.net",
    "wss://nostr.mom",
    "wss://relay.nostr.band",
    "wss://nos.lol",
    "wss://relay.nostr.com.au",
    "wss://relay.mostr.pub",
    "wss://nostr.milou.lol",
    "wss://relay.nostr.net.in",
    "wss://nostr.slothy.win"
]

# Motivational messages
MESSAGES = [
    "Time for your daily 100 pushups! Let's get those gains! 💪 #Bitcoin #Fitness",
    "Stack sats and do pushups - building wealth and strength! 🏋️‍♂️ #Nostr #PersonalTrainer",
    "100 pushups a day keeps the doctor away! Stack gains and stack sats! 🏃‍♂️ #HealthyLifestyle #BTC",
    "Push yourself to new limits - 100 pushups and more sats in your wallet! 🚀 #Motivation #StackSats",
    "Strong body, strong mind, strong Bitcoin stack. Let's crush those pushups! 💯 #NostrFitness #HODL",
    "Every pushup brings you closer to your goals. Every sat brings you closer to financial freedom! 🎯 #BitcoinFitness",
    "Consistency is key - in fitness and in stacking sats. Keep pushing! 🔑 #DailyHabit #Bitcoiner",
    "Your future self will thank you for the pushups and the sats. Get to work! 🙏 #SelfImprovement #BTC100K",
    "Pain is temporary, gains are forever. Same goes for Bitcoin! 📈 #NostrMotivation #NumberGoUp",
    "100 pushups, 100k per Bitcoin - we're on our way! Keep stacking and keep pushing! 🚀 #BitcoinToTheMoon #FitnessGoals",
    "Push through the pain, stack those sats! 100 pushups, 100 satoshis. 🏋️‍♀️ #FitAndRich #BTCGoals",
    "Get stronger every day, both in body and in Bitcoin. 100 pushups, no excuses! 💥 #SatoshiStrong #FitnessChallenge",
    "Start the day with pushups and stacking sats! Double up on strength and savings! 💪💰 #MorningRoutine #BTCWarrior",
    "No pain, no gain – no risk, no Bitcoin. 100 pushups a day, let’s crush it! 🏆 #Bitcoin #100",
    "Strength in numbers – pushups and satoshis! Let’s get those 100 in today! 🔥 #Workout #HealthAndWealth",
    "Push yourself harder, stack sats faster! 100 pushups, let’s build that future! 🔨 #FinancialFitness #BTCStacker",
    "Success is built in small steps: pushups today, Bitcoin tomorrow! 🏋️‍♂️ #FitFinance #SatsAndSweat",
    "No shortcuts – to fitness or Bitcoin wealth. 100 pushups a day, every sat counts! 🎯 #GrindAndStack #BitcoinDaily",
    "Discipline leads to greatness. 100 pushups today, 1 Bitcoin in the future! 🏋️‍♀️ #DailyGrind #FitnessGoals",
    "From pushups to profit, stack your strength and sats every single day! 💪💸 #FitBitcoin #SatoshiSquad",
    "Rise and grind! 100 pushups await. Your future self thanks you.",
    "Bitcoin doesn't sleep, and neither does your workout routine! Keep pushing!",
    "Every sat stacked is a step towards freedom. Keep building that future! 🔑 #Bitcoin",
    "Pushups build strength, Bitcoin builds wealth. Why not do both? 💪💰",
    "100 pushups, 21 million Bitcoin. Scarcity drives value in fitness and finance! #BTC",
    "No excuses, just results. Whether it's fitness or Bitcoin, consistency is key.",
    "Stack sats, not excuses. Your financial future depends on it! 📈 #HODL",
    "Sweat now, shine later. True for both muscles and Bitcoin! 🏋️‍♂️",
    "Building a better you, one pushup at a time. Keep going!",
    "Bitcoin: the marathon, not the sprint. Pace yourself and keep stacking! 🏃‍♂️💰",
    "100 pushups today means a stronger you tomorrow. Start now!",
    "HODLing Bitcoin and holding planks - building a resilient future! 💪",
    "Every pushup counts, every sat matters. Small actions, big results! #BitcoinFitness",
    "Pain is temporary, Bitcoin is forever. Push through it! 🚀",
    "Your body is your own proof of work. 100 pushups, no shortcuts! #FitnessGoals",
    "Stack sats and build muscle - invest in yourself! 🏋️‍♀️",
    "Bitcoin doesn't judge, and neither does your workout. Just show up and do the work.",
    "100 pushups a day keeps the fiat away! 💪🔥 #BitcoinStrength",
    "Pushups and Bitcoin - two things you'll never regret starting early.",
    "Don't wait for the perfect moment. Start your pushups and start stacking now!",
    "Building strength in body and in Bitcoin. Future you will be grateful. #SatoshisAndSitups",
    "100 pushups, 1 sat at a time. Progress is progress, no matter how small.",
    "Strong body, strong mind, strong Bitcoin stack. Triple threat! 💯",
    "Each pushup makes you stronger. Each sat makes you freer. Keep going!",
    "Bitcoin and fitness: two paths to a better future. Which one will you choose today?",
    "No one ever regretted doing those extra pushups or buying more Bitcoin. Push harder!",
    "Your muscles and your Bitcoin wallet have one thing in common: they grow with patience and consistency.",
    "100 days of pushups, 100 weeks of stacking. Small habits, big changes. #BitcoinFitness",
    "Pushups build your chest, Bitcoin builds your nest. Invest in both! 💪💰",
    "Pushups and stacking sats: building strength and wealth one rep at a time! 💪💰",
    "Satoshi probably does 1000 pushups a day. You can do 100! 💪🏆",
    "Satoshi didn’t wait, and neither should you. 100 pushups, let’s go! 🚀",
    "Every sat counts, every pushup counts. Get stronger, stack smarter! 🔥",
    "HODL your Bitcoin, hold your form. 100 pushups, no excuses! 🏋️‍♂️",
    "Stacking sats and crushing pushups - the ultimate daily grind! 💯",
    "21 million Bitcoin, infinite pushup potential. Let’s hit 100 today! 💪💥",
    "Do 100 pushups today, stack sats for tomorrow. Health and wealth in one! 🏆",
    "Bitcoin's fixed supply, your unlimited gains. 100 pushups, let's move! 💸💪",
    "Sweat now, stack sats later. Fitness and Bitcoin are long-term games! 🏋️‍♀️",
    "Push your limits, stack your sats. Stronger body, stronger wallet! 💪🔥",
    "Tick tock, next block! Time to hit the floor for your daily pushups!",
    "Blocks are rolling in, and so should your pushups! Let’s stack reps like sats!",
    "Next block confirmed – time to confirm your gains with 100 pushups!",
    "Push through like the next Bitcoin block – 100 pushups, let’s go!",
    "Tick tock, the network’s on fire, and so are you! Hit those pushups!",
    "Every new block is a reminder – get stronger with every pushup!",
    "Blocks don’t wait, and neither should you! Time for pushups, let’s grind!",
    "Another block, another rep. Let’s get those pushups in and stack strength like sats!",
    "Bitcoin never stops, and neither do your pushups. Next block, next rep!",
    "Tick tock, pushup clock! 100 reps before the next block confirmation!",
    "Blocks are steady, pushups should be too! Time to power through!",
    "As the next block confirms, so do your daily pushups. No excuses!",
    "Tick tock, Bitcoin block! You’ve got 100 pushups waiting for you!",
    "The next block is coming in fast – faster than your pushup pace? Let’s go!",
    "Pushups and blocks – both build strong foundations. Time to work!",
    "Another block, another pushup – the grind doesn’t stop!",
    "Bitcoin’s on the move, are you? Time for your pushups, let's hit the floor!",
    "Next block inbound! Stack your sats and stack those pushups!",
    "Blocks are getting mined, and you’re getting stronger! Pushup time!",
    "Tick tock, next block – let’s crank out those 100 pushups, no slacking!",
    "New block on the way – your reminder to crush those pushups!",
    "Stack sats, stack reps. Pushups don’t wait, just like the next block!",
    "Tick tock, the blockchain’s moving – get your pushups in before the next block!",
    "The network is secure, are you? Time for your daily pushups!"
]

# Hashtags
HASHTAGS = [
    "#Bitcoin", "#Nostr", "#Fitness", "#PersonalTrainer", "#StackSats", "#Pushups",
    "#HealthyLifestyle", "#Motivation", "#BTC", "#NostrFitness", "#HODL",
    "#BitcoinFitness", "#DailyHabit", "#Bitcoiner", "#SelfImprovement", "#BTC100K",
    "#NostrMotivation", "#BitcoinToTheMoon", "#FitnessGoals", "#Bitcoin", "#Nostr", "#Fitness", "#PersonalTrainer", "#StackSats", "#Pushups",
    "#HealthyLifestyle", "#Motivation", "#BTC", "#NostrFitness", "#HODL",
    "#BitcoinFitness", "#DailyHabit", "#Bitcoiner", "#SelfImprovement", "#BTC100K",
    "#NostrMotivation", "#BitcoinToTheMoon", "#FitnessGoals",
    "#SatoshiStrong", "#BTCWarrior", "#FinancialFreedom", "#GymLife",
    "#BlockchainFitness", "#HODLStrong", "#BitcoinRevolution", "#FiatFree",
    "#SatStackingSunday", "#NostrNetwork", "#LightningNetwork",
    "#21Million", "#BitcoinStandard", "#DigitalGold", "#SoundMoney",
    "#Hyperbitcoinization", "#BTCPumped", "#NodeRunner", "#Sovereignty",
    "#EconomicFreedom", "#HardMoney", "#ProofOfWork", "#MusclesAndMining",
    "#BitcoinBeach", "#OrangeYourself", "#SweatEquity", "#SatoshiSquats",
    "#BlockchainBiceps", "#CypherpunkCardio", "#DecentralizedGains",
    "#PumpAndHODL", "#HashrateFitness", "#BitcoinBonds", "#NoKYCGains",
    "#P2PFitness", "#LowTimePrefLifestyle", "#StackingAndSquatting",
    "#BTCBeastMode", "#NostrNation", "#LNFitness", "#SelfCustody",
    "#BitcoinIronman", "#NostrGains", "#SatoshiSets", "#BlockchainBurn",
    "#HODLersHealth", "#BitcoinMarathon", "#NostrNinjas", "#SovereignStrength"
]

def create_nostr_event(content):
    event = Event(content)
    private_key = PrivateKey.from_nsec(NOSTR_PRIVATE_KEY)
    event.sign(private_key.hex())
    return event

def post_to_nostr(event, relay_manager):
    relay_manager.publish_event(event)
    relay_manager.run_sync()

def generate_message():
    message = random.choice(MESSAGES)
    extra_hashtags = " ".join(random.sample(HASHTAGS, 3))  # Add 3 random hashtags
    return f"{message}\n\n{extra_hashtags}"

def countdown_timer(seconds):
    start_time = time.time()
    end_time = start_time + seconds
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        hours, remainder = divmod(remaining_time, 3600)
        minutes, secs = divmod(remainder, 60)
        print(f"\rNext post in: {hours:02d}:{minutes:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)
    print("\nPosting now...")

def main():
    relay_manager = RelayManager()
    for relay in NOSTR_RELAYS:
        try:
            relay_manager.add_relay(relay)
            print(f"Successfully connected to {relay}")
        except Exception as e:
            print(f"Failed to connect to {relay}: {e}")

    while True:
        message = generate_message()
        event = create_nostr_event(message)
        try:
            post_to_nostr(event, relay_manager)
            print(f"Posted at {datetime.datetime.now()}: {message}")
        except Exception as e:
            print(f"Failed to post message: {e}")
        
        # Wait for 3-4 hours before the next post
        sleep_time = random.randint(3 * 3600, 4 * 3600)
        print(f"Waiting for {sleep_time // 3600} hours and {(sleep_time % 3600) // 60} minutes until next post.")
        countdown_timer(sleep_time)

if __name__ == "__main__":
    main()
