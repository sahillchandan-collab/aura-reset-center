import json
t=open('office.html').read()
W=[[1.5,3,31,42],[34.5,3,31,42],[67.5,3,31,42],[1.5,55,31,42],[34.5,55,31,42],[67.5,55,31,42]]
N=[[2,2,46,30],[52,2,46,30],[2,35,46,30],[52,35,46,30],[2,68,46,30],[52,68,46,30]]
def rooms(work):
    out=[]
    for i,(rid,name,about,floor) in enumerate(work+[("break","Break Room","Where free agents grab coffee between jobs.","break"),("board","Boardroom","The whole team meets here for board meetings and status reports.","board")]):
        out.append(dict(id=rid,name=name,about=about,floor=floor,w=W[i],n=N[i]))
    return out
def C(name,role,dept,pitch,skills,mind,shirt=""): return dict(name=name,role=role,dept=dept,pitch=pitch,skills=skills,mind=mind,shirt=shirt)
B=[
 dict(slug="yontro",title="Yontro HQ",name="Yontro",initial="Y",kind="Marketing agency · yontro.ae",accent="#FF5A1F",ink="#111111",dark="#FF6B35",
  goal="5 signed clients by 31 December 2026 (AED 25,000+ a month), so Yontro covers its AED 8,000 payroll.",status="red",note="0 contracts after one month · 4 warm prospects",
  about="Social media marketing agency, Yontro - F.Z.E (Ajman Free Zone), office in Business Bay, Dubai. Packages Launch AED 5,000 / Growth 7,500 / Scale 10,000 a month, paid in advance, 3-month standard term (1-2 months by exception). Sales: cold calling and visits by Usama Rehman offering a free video, plus Meta ads. Azeem Shafi is the videographer. Started 19 October 2026, no contracts signed yet. Account manager role open.",
  rooms=rooms([("sales","Sales Floor","Pipeline, calls, follow-ups and closes.","a"),("studio","Video Studio","Shoot plans, shot lists and edits.","c"),("content","Content Lab","Case studies, captions, calendars and ad creative.","b"),("research","Research Desk","Prospect lists and pre-meeting briefs.","d")]),
  agentDept={"sales-manager":"sales","content-strategist":"content","lead-researcher":"research"},
  candidates=[C("Tariq Saleh","Closer · Senior Account Executive","sales","Joins tough meetings and turns warm prospects into signed 3-month contracts.",["Objection handling","Proposals","Negotiation"],"Close with confidence: restate the prospect's pain, show the case study, offer the 1-month starter term only when needed. Always end with a clear next step and date."),
   C("Mei Lin","Meta Ads Specialist","content","Builds and tunes lead-gen campaigns for the free-video offer.",["Meta Ads","Copy testing","Lead forms"],"Write ad sets for Dubai SME owners; test 3 hooks; report cost per lead and booked meeting, not likes."),
   C("Joel Fernandes","Shoot Producer","studio","Plans shoots so Azeem gets three great videos out of one visit.",["Shot lists","Scheduling","Storyboards"],"Plan every shoot: hook, b-roll list, location notes, timing. Keep it doable in 90 minutes."),
   C("Aisha Qureshi","Account Manager","content","Looks after signed clients: onboarding, monthly calendars and reporting.",["Onboarding","Calendars","Client reports"],"Clients first: clear monthly calendar, weekly update, monthly results report with views and enquiries."),
   C("Marco Bianchi","Cold Outreach Writer","sales","Writes WhatsApp and email openers that get replies.",["WhatsApp scripts","Email","Follow-ups"],"Short, specific, personal. One question per message. Mention the free video and a result from a similar business.")]),
 dict(slug="botany",title="Botany Properties HQ",name="Botany Properties",initial="B",kind="Real estate · management and advisory",accent="#2E6B4F",ink="#ffffff",dark="#5DBB8C",
  goal="By 31 December 2026: every overdue rent collected or in the legal process, every vacant flat let, monthly statements going to both owners. Then 5 investor meetings a week.",status="red",note="No rental register yet · amounts owed unknown",
  about="Dubai real estate company: property management at 10% of yearly rent, and investment advisory (2% acquisition commission). Partner Mia (videos and ads). Holds POA for owners Panagiotis Evangelinos and Georgios Boktor; problems are vacant flats, overdue rent and bounced cheques needing legal action (returned-cheque certificate, formal notice, RDSC, execution judge; confirm with a lawyer). Investor client Mr Hashim has a 5-year Al Manara Tower (JVT) plan.",
  rooms=rooms([("rentals","Rentals Desk","The rental register, cheques, rents and owner statements.","a"),("legal","Legal Room","Demand notices, RDSC files and lawyer follow-ups.","c"),("investors","Investor Lounge","Investment plans, yields and client meetings.","b"),("media","Media Room","Listings, photos and videos with Mia.","d")]),
  agentDept={"property-manager":"rentals","legal-assistant":"legal","investor-advisor":"investors"},
  candidates=[C("Nadia Haddad","Leasing Agent","rentals","Gets vacant flats listed, viewed and let within 30 days.",["Listings","Viewings","Pricing"],"Price to let in 30 days. Write listings for Property Finder and Bayut, schedule viewings, qualify tenants."),
   C("Samir Aziz","Collections Officer","legal","Chases overdue rent firmly and politely, and logs every step.",["Payment plans","Notices","Follow-up logs"],"Firm and polite. Offer a payment plan before escalating. Log every contact with date and amount."),
   C("Grace Lim","Owner Relations Manager","rentals","Keeps Panagiotis and Georgios informed and confident.",["Owner statements","Updates","Renewals"],"Monthly statement per owner: rent received, arrears, actions, next steps. Calm and transparent."),
   C("Hassan Javed","Real Estate Content Producer","media","Turns Mia's market knowledge into short investor videos.",["Scripts","Reels","Market explainers"],"60-second scripts on Dubai investing: yields, JVT, equity release. One clear takeaway per video."),
   C("Olivia Brooks","Mortgage and Finance Analyst","investors","Models equity release and loan scenarios for investors.",["LTV","Cash flow","Bank comparisons"],"Conservative numbers. Show monthly cash flow, LTV and the worst case.")]),
 dict(slug="foundertales",title="Founder Tales HQ",name="Founder Tales",initial="F",kind="Media brand · foundertales.ae",accent="#C8902A",ink="#111111",dark="#E3B04B",
  goal="2,000 followers by 30 November 2026 · 5,000 followers and the first paid feature sold by 31 March 2027.",status="amber",note="About 1,000 followers · no website or sales kit yet",
  about="Founder-story media brand for young entrepreneurs, about 1,000 followers (November 2026). Azeem Shafi makes 3 videos a day. Plan: grow, then sell paid feature episodes to founders (needs a website and a sales kit with rate card), later a news publication and an exclusive founders network with an acquisition model.",
  rooms=rooms([("studio","Studio","Story ideas, hooks and shoot plans.","a"),("edit","Edit Bay","Edits, captions, thumbnails and posting.","c"),("partners","Partnerships","Paid features, media kit and founder sales.","b"),("web","Newsroom","Website, articles and the future publication.","d")]),
  agentDept={"growth-manager":"studio","partnerships":"partners"},
  candidates=[C("Zara Ahmed","Story Producer","studio","Finds founders with stories worth telling and writes the angle.",["Research","Interviews","Story arcs"],"Every story needs a turning point. Find it, write the hook in 8 words, plan a 60-second arc."),
   C("Leo Martins","Short-form Editor","edit","Cuts videos that keep people watching to the end.",["Hooks","Captions","Pacing"],"First 2 seconds decide everything. Suggest cuts, on-screen text and captions for each video."),
   C("Priya Nair","Founder Partnerships Manager","partners","Sells feature episodes to Dubai founders.",["Outreach","Media kit","Pricing"],"Lead with audience proof. Pitch the feature episode; upsell article and boosted reach."),
   C("Sam Wright","Editor-in-Chief","web","Plans the website and the future Founder Tales publication.",["Editorial","SEO","Newsletters"],"Clear, useful writing for young founders. Build the content plan around evergreen founder lessons."),
   C("Noura Al Habtoor","Community Manager","edit","Replies, DMs and collabs that turn viewers into followers.",["Engagement","Collabs","DMs"],"Reply fast and personally. Find 5 collab accounts a week. Track follower growth daily.")]),
 dict(slug="aura",title="Aura Wellness HQ",name="Aura Wellness Center",initial="A",kind="Wellness center · Sahill is GM",accent="#6E5BA8",ink="#ffffff",dark="#A795E0",
  goal="Monthly revenue above the AED 170,833 break-even, then a 20% margin (about AED 205,000 a month).",status="grey",note="No revenue figures shared yet",
  about="Wellness center in Dubai where Sahill is General Manager. Monthly running costs about AED 170,833: rent AED 730,000 a year (60,833 a month), salaries 80,000, DEWA 10,000, marketing 10,000, other 10,000. Sales-boost levers: off-peak offers, corporate wellness packages, memberships over one-offs, referrals and Google reviews, content and Meta ads run by Yontro tracked on bookings.",
  rooms=rooms([("front","Front Desk","Bookings, walk-ins, reviews and guest experience.","a"),("members","Memberships","Packages, renewals and the break-even tracker.","c"),("corporate","Corporate Sales","Company wellness deals and partnerships.","b"),("marketing","Marketing","Offers, content and bookings-focused ads.","d")]),
  agentDept={"gm-assistant":"members","corporate-sales":"corporate"},
  candidates=[C("Layla Karim","Guest Experience Lead","front","Turns first-time visitors into members and happy reviewers.",["Reviews","Follow-ups","Upsells"],"Every visit ends with a review ask and a next booking. Warm, calm, premium tone."),
   C("Ethan Cole","Retention Analyst","members","Spots members about to leave and wins them back.",["Churn","Win-back offers","Renewals"],"Find who hasn't visited in 3 weeks; draft a personal win-back message and offer."),
   C("Maryam Siddiqui","Partnerships Manager","corporate","Partners with gyms, hotels and clinics for referrals.",["Partnerships","Referral deals","Events"],"Find partners whose clients want wellness; propose simple referral deals with clear numbers."),
   C("Diego Alvarez","Performance Marketer","marketing","Runs bookings-focused ads with Yontro.",["Meta Ads","Offers","Tracking"],"Measure cost per booking. Test off-peak offers. Kill what doesn't book."),
   C("Sara Johansson","Pricing Strategist","members","Designs memberships and packages that cover the break-even.",["Pricing","Packages","Break-even"],"Work from AED 170,833 a month. Show how many memberships or sessions close the gap.")]),
 dict(slug="barter",title="Barter HQ",name="Barter",initial="B",kind="Car-swap marketplace · idea stage",accent="#1F5FBF",ink="#ffffff",dark="#5B93E8",
  goal="Prove demand with 50 car listings and 3 completed swaps before building any app.",status="parked",note="Idea stage, until Yontro and Botany are green",
  about="Idea-stage marketplace app in the UAE where people swap cars instead of selling for cash, with cash top-ups for value differences. Open questions: demand, fair valuation (inspection partner), RTA transfer, insurance and car loans, how Barter earns (listing fee, swap fee, inspection and transfer service, finance referrals), competition (dubizzle, CarSwitch, dealer trade-ins). Long-term aim: raise VC funding or sell.",
  rooms=rooms([("lab","Research Lab","Market research, interviews and validation data.","a"),("market","Market Desk","Listings, matching and the demand test.","c"),("product","Product Room","Concept, MVP scope and user flows.","b"),("partners","Partners Desk","Inspection, finance and RTA partners.","d")]),
  agentDept={"research-analyst":"lab"},
  candidates=[C("Kenji Watanabe","Product Manager","product","Turns the concept into a lean MVP scope.",["MVP scoping","User flows","Roadmaps"],"Smallest thing that proves swaps happen. Cut everything else."),
   C("Fatma Yilmaz","Growth Tester","market","Runs the Instagram and form demand test.",["Landing pages","Forms","Instagram"],"Aim for 50 listings. Track listings, matches and completed swaps weekly."),
   C("Ahmed Farouk","Automotive Partnerships Lead","partners","Brings in inspection, finance and transfer partners.",["Inspections","Car finance","RTA"],"Find partners that make swaps safe: valuation, loan settlement, RTA transfer."),
   C("Chloe Durand","Investor Relations Analyst","product","Builds the story and numbers for a future raise.",["Pitch decks","Market sizing","VC lists"],"Only raise on real traction. Size the UAE used-car market honestly.")]),
]
SUG={"yontro":["What's everyone working on?","Usama booked 3 meetings today, log it","Get Omar to write follow-ups for the 4 warm prospects now"],
 "botany":["Start the rental register now","Tenant in a flat bounced a cheque, what next?","What does Fatima need from me?"],
 "foundertales":["Give me today's 3 video ideas","We hit 1,200 followers, remember it","Have Amara draft the rate card now"],
 "aura":["Here are last month's numbers…","Build the corporate package now","Hire someone for Google reviews"],
 "barter":["What should we test first?","Have Elena write the one-page concept","Park Barter until January"]}
for b in B:
  biz={k:b[k] for k in ["name","kind","goal","status","note","about","rooms","agentDept","candidates"]}; biz["corridorY"]=50; biz["suggestions"]=SUG[b["slug"]]
  s=(t.replace('__TITLE__',b['title']).replace('__NAME__',b['name']).replace('__KIND__',b['kind'].upper()).replace('__INITIAL__',b['initial'])
      .replace('__ACCENT__',b['accent']).replace('__ACCENT_INK__',b['ink']).replace('__ACCENT_DARK__',b['dark']).replace('__GOAL__',b['goal'])
      .replace('__BIZJSON__',json.dumps(biz).replace('</','<\\/')))
  assert '__' not in s.split('<script>')[0] and '__BIZJSON__' not in s
  open(f"{b['slug']}.html",'w').write(s)
print('built')
