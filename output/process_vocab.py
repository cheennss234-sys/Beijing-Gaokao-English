#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process collected exam texts to generate extracurricular vocabulary frequency list.
- Tokenize, lemmatize (conservative rule-based), remove stopwords & textbook vocabulary
- Count frequencies, keep freq >= 3
- Sort by frequency (desc), then alphabetically
"""

import re
import os
import json
from collections import Counter

# ============ Stopwords (checked BEFORE lemmatization) ============
STOPWORDS = set("""
a about above after again against all am an and any are aren't as at be because been before being below between both but by can can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves
this these those there here where when why how what which who whom whose
is am are was were be been being have has had do does did done doing go goes went gone going come comes came coming get gets got gotten getting make makes made making take takes took taken taking see sees saw seen seeing know knows knew known knowing think thinks thought thinking say says said saying give gives gave given giving find finds found finding tell tells told telling become becomes became becoming leave leaves left leaving feel feels felt feeling put puts putting bring brings brought bringing begin begins began begun beginning keep keeps kept keeping hold holds held holding write writes wrote written writing stand stands stood standing hear hears heard hearing let lets letting mean means meant meaning set sets setting meet meets met meeting run runs ran running pay pays paid paying sit sits sat sitting speak speaks spoke spoken speaking show shows showed shown showing read reads reading spend spends spent spending grow grows grew grown growing lose loses lost losing fall falls fell fallen falling cut cuts cutting reach reaches reached reaching raise raises raised raising move moves moved moving live lives lived living play plays played playing happen happens happened happening look looks looked looking seem seems seemed seeming help helps helped helping turn turns turned turning start starts started starting try tries tried trying call calls called calling use uses used using want wants wanted wanting need needs needed needing work works worked working seem seems seemed seeming
also however therefore thus moreover meanwhile furthermore nevertheless nonetheless otherwise instead still already yet ever never always often sometimes usually frequently rarely seldom now then today tomorrow yesterday soon later recently eventually finally ultimately here there everywhere anywhere somewhere nowhere
something anything everything nothing someone anyone everyone nobody somebody anybody everybody anybody somewhere anywhere everywhere nowhere
another other such same different similar various particular certain specific general common ordinary normal usual regular typical
whether either neither both each every all none some most few many several much more less least
after before during while since until upon among between within without across through along around behind beyond beside near
""".split())

# ============ Textbook vocabulary (人教版 + 北师大版 高中英语) ============
TEXTBOOK_VOCAB = set("""
ability able about above abroad absence absent absolute accept access accident account accuse achieve achievement acid across act action active activity actual actually adapt add addition additional address adequate adjust admire admit adopt adult advance advantage adventure advertise advice advise affair affect afford afraid after afternoon again against age agency agent ago agree agreement ahead aid aim air airline airport alarm album alcohol alive all allow almost alone along already also although altogether always amaze amazing ambition among amount amuse analysis analyze ancient anger angle angry animal ankle anniversary announce annual another answer anxiety anxious any anybody anyhow anyone anything anyway anywhere apart apartment apologize appeal appear appearance apple application apply appoint appreciate approach appropriate approve approximately archaeology architect architecture area argue argument arise arm army around arrange arrest arrive arrow art article artist as ash ask aspect assess assignment assist associate assume astronaut astronomy at athlete atmosphere attach attack attempt attend attention attitude attract attractive audience August aunt Australia Australian author authority autumn available avenue average avoid awake award aware away awful baby back background backward bad badminton bag baggage bake balance ball balloon ban band bank bar barbecue bare bargain barrier base basic basis basket basketball bath bathe battle bay be beach bean bear beat beautiful beauty because become bed bedroom bee beef beer before beg begin behave behaviour behind being belief believe bell belong below belt bench bend beneath benefit beside besides best bet better between beyond bicycle big bike bill billion biology bird birth birthday biscuit bit bite bitter black blame blank blanket bleed blend bless blind block blood blouse blow blue board boat body boil bomb bone book boom boot border boring born borrow boss both bother bottle bottom bounce bow bowl box boy brain branch brand brave bread break breakfast breast breath breathe breed brick bridge brief bright bring broad broadcast brother brown brush bubble budget build building bullet bunch burden burn burst bury bus business busy but butter button buy by cab cabbage cable cafe cage cake calculate call calm camera camp campaign campus can canal cancel cancer candidate candle candy cap capable capital captain capture car card care career careful careless carrot carry case cash cast castle cat catch category cause cave ceiling celebrate cell cent center central century ceremony certain certainly chain chair chairman challenge chamber champion chance change channel chapter character charge charity chart chase cheap cheat check cheek cheer cheese chef chemical chemistry cheque cherry chess chest chew chicken chief child childhood chimney chip chocolate choice choose chopsticks church cigarette cinema circle circuit citizen city civil claim class classic classical classroom clean clear clerk clever click client climate climb clinic clock close cloth clothes clothing cloud club coach coal coast coat code coffee coin cold collapse collar colleague collect collection college color colour comb combine come comedy comfort comfortable command comment commercial commit committee common communicate communication community company compare comparison compete competition complain complete complex complicated component compose composition comprehensive computer concept concern conclude conclusion concrete condition conduct conference confidence confirm conflict confuse connect connection consequence consider consist constant construct construction consult consume consumer contact contain content contest context continent continue contract contradiction contrast contribute control convenient conversation convince cook cool cooperate copy core corn corner corporate correct cost cottage cotton could council count country countryside county couple courage course court cousin cover cow crash crazy cream create creative creature credit crew crime criminal crisis critic critical criticism crop cross crowd crowded cruel cry culture cup cure curious current curtain curve custom customer cut cute cycle
dad daily damage dance danger dangerous dare dark data date daughter day dead deadline deaf deal dear death debate debt decade decide decision declare decline decorate decoration decrease deep deer defeat defend defense define definite definitely degree delay delete delicious deliver demand democracy demonstrate dentist deny depart department depend deposit depth describe description desert design desire desk desperate despite dessert destination destroy destruction detail detect determine develop development device devote dialogue diamond diary dictionary die diet differ difference different difficult difficulty dig digital dignity dimension dine dinner direct direction director dirt dirty disabled disadvantage disagree disappear disappoint disaster discipline discount discover discovery discuss discussion disease dish disk dismiss display distance distant distinct distinguish distribute district disturb divide division divorce do doctor document dog doll dollar domestic door double doubt down download downtown dozen draft drag drama draw drawer dream dress drill drink drive driver drop drug drum dry duck due dull during dust duty
each ear early earn earth ease east eastern easy eat economic economy edge edit education effect effective effort egg eight either elder elect electric electronic elegant element elephant elevator else email embarrass embassy emerge emergency emotion emotional emperor emphasis employ employee employer employment empty enable encourage end endless enemy energy engage engine engineer England English enjoy enormous enough ensure enter enterprise entertainment entire entrance entry environment equal equipment era error escape especially establish estate Europe European evaluate even evening event eventually ever every everybody everyone everything everywhere evidence evident evil evolution evolve exact exactly examination examine example excellent except exchange excite exciting exclude excuse execute exercise exhibit exhibition exist existence exit expand expansion expect expectation expense expensive experience experiment expert explain explanation explore explosion export expose express expression extend extension extensive extra extraordinary extreme extremely eye eyesight
fable face facility fact factor factory fail failure fair fairly faith fall false familiar family famous fan fancy fantastic far farm farmer fashion fast fat fate father fault favor favourite fear feature fee feed feel feeling fellow female fence festival fetch fever few field fierce fight figure file fill film final finance financial find fine finger finish fire firm first fish fit five fix flag flame flash flat flavor flee flexible flight float flood floor flour flow flower flu focus fog fold follow following fond food fool foolish foot football for forbid force forecast forehead foreign forest forever forget forgive form formal former formula fort forth fortune forty forward found foundation fountain four fox fragile frame free freedom freeze frequent fresh friend friendly friendship frog from front frozen fruit fry fuel full fun function fund fundamental funeral funny furniture further future
gain gallery game gang gap garage garbage garden gas gate gather gay gaze gear gender gene general generation generous gentle gentleman genuine geography gesture get ghost giant gift girl give glad glance glass globe glory glove go goal goat god gold golden golf good goodbye goods goose govern government grade gradually graduate grain grammar grand grandfather grandmother grant grape graph grasp grass grateful gravity gray great green greet greeting ground group grow growth guarantee guard guess guest guide guilt guitar gun guy
habit hair half hall hammer hand handful handle hang happen happy hard hardly harm hat hate have he head headache headline health healthy hear heart heat heavy height hello help helpful her here hero hesitate hide high highlight hike hill him hire his history hit hold hole holiday home homeless honest honey honor hope horrible horse hospital host hot hotel hour house household housing how however huge human humor hundred hungry hunt hurry hurt husband
ice idea ideal identify identity if ill illegal illness image imagine immediate immediately immigrant impact imply import importance important impose impossible impress impression improve improvement in incident include income increase indeed independent index indicate indication individual industrial industry inevitable infection influence inform information ingredient initial injury inner innocent input inquiry inside insist inspire install instance instead institute institution instruct instruction instrument insurance intellectual intelligence intelligent intend intense intention interest interesting interior internal international internet interpret interpretation interrupt interview into introduce introduction invade invent invention invest investigate invitation invite involve iron island issue it item its itself
jacket jam January jazz jealous jeans jet job join joint joke journal journalist journey joy judge juice July jump June junior jury just justice justify
keep key keyboard kick kid kill kilo kind king kiss kitchen knee knife knock know knowledge
lab label labor laboratory lack ladder lady lake lamp land landlord language large last late later latter laugh launch law lawn lawyer lay layer lazy lead leader leadership leaf league lean learn least leather leave lecture left leg legal legend legislation leisure lemon lend length less lesson let letter level liberal library license lie life lifestyle lifetime lift light like likely limit limited line link lion lip list listen literature little live lively living load loan local locate location lock log logic logical lonely long look loose lose loss lost lot loud love lovely low lower loyal luck lucky lunch lung
machine mad magazine magic mail main mainly maintain major majority make male man manage management manager manner manual manufacture many map march mark market marriage married marry mask mass master match material math matter maximum may maybe mayor me meal mean meaning means measure meat medal media medical medicine medium meet meeting member memory mental mention menu mere merely message metal method middle might mild military milk million mind mine mineral minister minor minority minute mirror miss mission mistake mix mixture mobile model modern modest mom moment money monitor monkey month mood moon moral more morning most mother motion motor mount mountain mouse mouth move movement movie much mud multiple murder muscle museum music musician must mutual myself mystery
nail name narrow nation national native natural nature near nearly neat necessary neck need needle negative negotiate neighbor neighborhood neither nephew nerve nervous network never new news newspaper next nice niece night nine no nobody nod noise none noon nor normal north northern nose not note nothing notice novel now nowhere nuclear number nurse nut
object objective observation observe obtain obvious obviously occasion occupy occur ocean odd of off offer office officer official often oh oil OK old Olympic on once one onion online only onto open opening operate operation opinion opportunity oppose opposite option or orange order ordinary organ organic organization organize origin original other otherwise ought our ours out outcome outdoor outer outline outside over overcome owe own owner
pace pack package page pain painful paint painting pair palace pale pan panel panic paper paragraph parcel parent park part participate particular particularly partner party pass passage passenger passion past path patient pattern pause pay payment peace peaceful peach peak pen pencil people pepper per percent perfect perform performance perhaps period permanent permit person personal personality persuade pet phase phenomenon philosophy phone photo photograph phrase physical physician piano pick picture piece pig pigeon pile pill pillar pilot pin pink pioneer pipe pitch pity place plain plan plane planet plant plastic plate platform play player please pleasure plenty plot plus pocket poem poet poetry point pole police policy polite political politics pollute pollution pool poor pop popular population port portable portrait position positive possess possible post pot potato potential pound pour poverty powder power powerful practical practice praise pray precious precise predict prefer pregnant prepare presence present preserve president press pressure pretend pretty prevent previous price pride primary prime principal principle print prior priority prison private prize probably problem process produce product production profession professional professor profit program project promise promote prompt proof proper properly property proposal propose protect protein protest proud prove provide province public publish pull purchase pure purpose pursue push put puzzle
quality quantity quarter queen question quick quickly quiet quietly quit quite quiz
race radiation radio rail rain raise range rank rapid rare rate rather raw reach react reaction read reader ready real reality realize really reason reasonable recall receive recent recently recognition recognize recommend record recover red reduce refer reference reflect reform refresh refuse regard region register regret regular regulate reject relate relation relationship relative relax release relevant relief rely remain remarkable remember remind remote remove rent repair repeat replace reply report reporter represent require research reserve resist respect respond response responsibility rest restaurant restore restrict result retire return reveal review revolution reward rice rich ride right ring rise risk river road rock role roll romantic roof room root rope rose rough round route row royal rub rule run runner rush
sad safe safety sail salad salary sale salt same sample sand save say scale scare scene schedule scheme scholarship school science scientific scientist scope score screen sea search season seat second secret secretary section secure security see seed seek seem segment seize select self sell send senior sense sensitive sentence separate September series serious serve service session set settle seven several severe shade shadow shake shall shallow shame shape share sharp she sheet shelf shell shelter shine ship shirt shock shoe shoot shop shore short shot should shoulder shout show shower shut shy sick side sigh sight sign signal silence silent silver similar simple simply since sing single sink sir sister sit site situation six size skate skill skin sky slave sleep slice slide slight slightly slip slow slowly small smart smell smile smoke smooth snap snow so social society soft software soil soldier solid solution solve some somebody someone something sometimes somewhere son song soon sorry sort soul sound source south southern space speak special specific speech speed spell spend spill spin spirit spiritual split sport spot spread spring square stable staff stage stair stand standard star stare start state statement station stay steady steal steam steel step stick still stock stomach stone stop store storm story straight strange strategy stream street strength strengthen stress stretch strict strike string strong structure struggle student studio study stuff stupid style subject submit succeed success successful such sudden suddenly suffer sufficient sugar suggest suggestion suit suitable summer sun super supply support suppose sure surface surgery surprise surround survey survive suspect suspend swallow swap swear sweep sweet swim swing switch symbol sympathy system
table tablet tail take tale talent talk tall tank tap tape target task taste tax taxi tea teach teacher team tear technique technology teen teenager telephone television tell temperature temporary ten tend tendency tennis tension term terrible test text than thank that the theater their them theme themselves then theory there therefore these they thick thin thing think third this though thought thousand threat threaten three throat through throughout throw thumb thunder thus ticket tide tie tight time tiny tip tired title to today together tomato tomorrow tone tongue tonight too tool tooth top topic total totally touch tough tour tourist toward tower town toy trace track trade tradition traditional traffic train training transfer transform translate transport trap travel treasure treat treatment tree trend trial triangle trick trip troop trouble truck true trust truth try tube turn TV twelve twenty twice twin twist two type typical
ugly umbrella unable uncle under undergo understand understanding uniform union unique unit unite universe university unless until unusual up update upon upper urban urge us use used useful useless user usual usually
vacation valid valley valuable value variety various vary vast vegetable vehicle venture very victim victory video view village violence virtual virtue virus visible vision visit visual vital voice volume volunteer vote
wage wait wake walk wall wallet wander want war warm warn wash waste watch water wave way we weak weakness wealth weapon wear weather web wedding Wednesday week weekend weekly weigh weight welcome welfare well west western what whatever wheat wheel when whenever where whereas whether which while whisper white who whole whom whose why wide widely wife wild will win wind window wine wing winner winter wipe wire wise wish with withdraw within without witness woman wonder wonderful wood wooden word work worker world worry worse worst worth would wound wrap write writer wrong
yard year yellow yes yesterday yet you young your yours yourself youth
zero zone zoo
abandon abstract academic accomplish acquire adequate administration admission affection aggressive agriculture alcohol alternative ambiguous analyze anonymous apparent appliance appropriate arbitrary aspect assist attain attribute authentic automatic behalf biology cabinet cancel capacity career caution civilization clarify comedy component conservative contemporary curriculum debate declare define demonstrate depart deposit describe design desire destroy detail detect determine device devote differ dimension disable discover discuss disease display distribute disturb domestic dominate donate drama dynamic economy edit educate efficient elaborate element eliminate emerge emphasis encourage enhance enormous ensure enter entertain entire environment equip erase essential establish estimate ethnic eventually evidence evolve exaggerate exceed exchange exclude exhibit expand expect experiment explain explore export expose express extend extent facility factor failure familiar fascinate fatal federal figure finance flavor flexible forbid forecast former fortune foundation fragment frequent function generate genuine global grade gradual graduate guarantee handle harvest hesitate highlight honor horizon identify identity ignore illustrate imagine immigrate impact imply import incident indicate individual industry inevitable influence inform initial injury innocent inspire install instance institute instruct instrument intelligent intend intense internal interpret interrupt interview introduce invade invest involve journal journey justify label labor launch lecture legal leisure level liberal license limitation literature locate maintain major manage manufacture margin mature measure medical medium mention merchant mercy method military minimum minor minute mission modern modest monitor motion motive mountain multiple murder mutual mystery narrative negative negotiate neighbor nervous neutral noble normal nuclear object observe obtain obvious occasion occupy occur official operate opinion oppose option organize origin original outline output overall overcome participate particular partner passage passion passive patient pattern pause peace permanent permit personal perspective philosophy phenomenon physical pioneer platform pleasant political popular population portrait possess potential prefer prepare present preserve pressure pretend prevent primary principle priority private procedure process produce profession profit program promote proof property propose protect provide publish purchase qualify quality quantity quote radical random range rank rapid rare rate ratio react realistic reason recall receive recent recognize recommend recover reduce refer reflect reform refuse regard region register regulate reject relate relax release relevant relief rely remain remark remind remote remove renew repair repeat replace represent require research resemble reserve resist resource respond restore restrict result retain retire reveal review revolution rigid routine sacrifice salary satisfy schedule scheme scholarship science score secure select senior sensitive separate sequence settle signal significant similar simple sincere situation social solar solution solve somehow source special specific sponsor stable standard statistic status straight strategy strength stress struggle submit substance succeed sufficient suggest superior suppose survive suspect sustain symbol sympathy talent technique tendency theory tolerate topic tradition tragic transfer transform translate transport treat trend trial unique unite universe unusual urgent valid valuable variety various vehicle venture violent virtual vital volunteer wander wealth welfare witness
""".split())

# ============ Header/metadata words to filter ============
HEADER_WORDS = set("""
cloze comprehension passage section grammar reading fill blank exam english chinese china beijing
yimo ermo midterm final mock district districta districtb region area part text answer question
choice correct option true false page word exercise test paper
""".split())

# ============ Web/OCR artifacts to filter (non-words, URL fragments, site names) ============
ARTIFACTS = set("""
com cn org net www http https html pdf jpg png url link click download
cnjy gaokzx doubaocdn cdn zizzs aka deepseek knull aisp cvp cxk ich mrf ssp
bteh jiaoxi jinchutou saam fao pre non eco apps app ceo
haidian xicheng dongcheng chaoyang fengtai shijingshan tongzhou daxing changping
shijingshan mentougou huairou pinggu miyun yanqing shunyi
shitiku yuekao qimo gaokao zhongkao gaozhong sanmo qizhong
didn don wasn couldn wouldn shouldn hasn haven isn aren weren doesn hadn
aas fesr fes hra asa nee eee bbd bik ses sra gea aaas
arr bes brak lar res sar arse bem bie dus eae ial mes peng sro tko bir
bma ces ees els esr ina ita laur tee aeb ais ama andr ans arie ata bel cse
ebm eme fea fer fre hee ipe iwas jer joh jre mhra mra mre rea ree saar seo sha
ll ve re t mrs phd rpm
""".split())

# ============ Proper nouns to filter (names, places, brands) ============
PROPER_NOUNS = set("""
beijing china chinese english america american europe european france french germany german
russia russian japan japanese korea korean india indian africa african australia australian
tsinghua olympic unesco london paris york washington boston virginia california
david mia rebecca laura sasha clara anne brookdale cleo kevin lina eric robbins
zhu yang jiaozi zha xca mengxiang drake egbert glenda raphael savitz jill
samantha rio ruth joy
brandon catherine danny dimeo hugh henry wilson susan alex dunn max tang
george leo regina renwick steven jake marcus nahmias nosek byrne kofi kung
hannah jessica milo smith huang zhao shanghai shanxi april december friday sunday
november christmas amazon zumba yoga pomodoro hogarth
anna mira brittany gertrude luke joyce squier william wyoming chicago schroeder chrystal
wukong xuhua
jack norton aria larry maya naidoo samuel wyatt emily robert tim travaris sumi blumberg
clarice gombeau kingsport lexi rikki rinehold sam sara austin amiri dube goldstein lewis
mcmillan minmier raynor england october september july monday
""".split())

# ============ Contractions expansion ============
CONTRACTIONS = {
    "don't": 'do', "doesn't": 'do', "didn't": 'do',
    "won't": 'will', "wouldn't": 'will',
    "can't": 'can', "couldn't": 'can',
    "shouldn't": 'should', "mustn't": 'must',
    "isn't": 'be', "aren't": 'be', "wasn't": 'be', "weren't": 'be',
    "haven't": 'have', "hasn't": 'have', "hadn't": 'have',
    "I'm": 'be', "i'm": 'be', "you're": 'be', "we're": 'be', "they're": 'be',
    "it's": 'be', "he's": 'be', "she's": 'be', "that's": 'be', "there's": 'be', "here's": 'be',
    "I've": 'have', "you've": 'have', "we've": 'have', "they've": 'have',
    "I'll": 'will', "you'll": 'will', "he'll": 'will', "she'll": 'will', "we'll": 'will', "they'll": 'will',
    "I'd": 'would', "you'd": 'would', "he'd": 'would', "she'd": 'would', "we'd": 'would', "they'd": 'would',
    "let's": 'let',
    "what's": 'be', "who's": 'be', "where's": 'be', "when's": 'be', "why's": 'be', "how's": 'be',
}

# ============ Irregular forms ============
IRREGULAR = {
    'was': 'be', 'were': 'be', 'been': 'be', 'being': 'be', 'am': 'be', 'is': 'be', 'are': 'be',
    'had': 'have', 'has': 'have', 'having': 'have',
    'did': 'do', 'does': 'do', 'doing': 'do', 'done': 'do',
    'said': 'say', 'saying': 'say', 'says': 'say',
    'went': 'go', 'gone': 'go', 'going': 'go', 'goes': 'go',
    'got': 'get', 'getting': 'get', 'gotten': 'get', 'gets': 'get',
    'made': 'make', 'making': 'make', 'makes': 'make',
    'knew': 'know', 'known': 'know', 'knowing': 'know', 'knows': 'know',
    'thought': 'think', 'thinking': 'think', 'thinks': 'think',
    'took': 'take', 'taken': 'take', 'taking': 'take', 'takes': 'take',
    'saw': 'see', 'seen': 'see', 'seeing': 'see', 'sees': 'see',
    'came': 'come', 'coming': 'come', 'comes': 'come',
    'found': 'find', 'finding': 'find', 'finds': 'find',
    'gave': 'give', 'given': 'give', 'giving': 'give', 'gives': 'give',
    'told': 'tell', 'telling': 'tell', 'tells': 'tell',
    'became': 'become', 'becoming': 'become', 'becomes': 'become',
    'left': 'leave', 'leaving': 'leave', 'leaves': 'leave',
    'felt': 'feel', 'feeling': 'feel', 'feels': 'feel',
    'brought': 'bring', 'bringing': 'bring', 'brings': 'bring',
    'began': 'begin', 'begun': 'begin', 'beginning': 'begin', 'begins': 'begin',
    'kept': 'keep', 'keeping': 'keep', 'keeps': 'keep',
    'held': 'hold', 'holding': 'hold', 'holds': 'hold',
    'wrote': 'write', 'written': 'write', 'writing': 'write', 'writes': 'write',
    'stood': 'stand', 'standing': 'stand', 'stands': 'stand',
    'heard': 'hear', 'hearing': 'hear', 'hears': 'hear',
    'meant': 'mean', 'meaning': 'mean', 'means': 'mean',
    'met': 'meet', 'meeting': 'meet', 'meets': 'meet',
    'ran': 'run', 'running': 'run', 'runs': 'run',
    'paid': 'pay', 'paying': 'pay', 'pays': 'pay',
    'sat': 'sit', 'sitting': 'sit', 'sits': 'sit',
    'spoke': 'speak', 'spoken': 'speak', 'speaking': 'speak', 'speaks': 'speak',
    'showed': 'show', 'shown': 'show', 'showing': 'show', 'shows': 'show',
    'spent': 'spend', 'spending': 'spend', 'spends': 'spend',
    'grew': 'grow', 'grown': 'grow', 'growing': 'grow', 'grows': 'grow',
    'lost': 'lose', 'losing': 'lose', 'loses': 'lose',
    'fell': 'fall', 'fallen': 'fall', 'falling': 'fall', 'falls': 'fall',
    'drove': 'drive', 'driven': 'drive', 'driving': 'drive', 'drives': 'drive',
    'rose': 'rise', 'risen': 'rise', 'rising': 'rise', 'rises': 'rise',
    'won': 'win', 'winning': 'win', 'wins': 'win',
    'wore': 'wear', 'worn': 'wear', 'wearing': 'wear', 'wears': 'wear',
    'ate': 'eat', 'eaten': 'eat', 'eating': 'eat', 'eats': 'eat',
    'drank': 'drink', 'drunk': 'drink', 'drinking': 'drink', 'drinks': 'drink',
    'slept': 'sleep', 'sleeping': 'sleep', 'sleeps': 'sleep',
    'flew': 'fly', 'flown': 'fly', 'flying': 'fly', 'flies': 'fly',
    'blew': 'blow', 'blown': 'blow', 'blowing': 'blow', 'blows': 'blow',
    'threw': 'throw', 'thrown': 'throw', 'throwing': 'throw', 'throws': 'throw',
    'drew': 'draw', 'drawn': 'draw', 'drawing': 'draw', 'draws': 'draw',
    'rode': 'ride', 'ridden': 'ride', 'riding': 'ride', 'rides': 'ride',
    'chose': 'choose', 'chosen': 'choose', 'choosing': 'choose', 'chooses': 'choose',
    'froze': 'freeze', 'frozen': 'freeze', 'freezing': 'freeze', 'freezes': 'freeze',
    'stole': 'steal', 'stolen': 'steal', 'stealing': 'steal', 'steals': 'steal',
    'hid': 'hide', 'hidden': 'hide', 'hiding': 'hide', 'hides': 'hide',
    'forgot': 'forget', 'forgotten': 'forget', 'forgetting': 'forget', 'forgets': 'forget',
    'forgave': 'forgive', 'forgiven': 'forgive', 'forgiving': 'forgive', 'forgives': 'forgive',
    'broke': 'break', 'broken': 'break', 'breaking': 'break', 'breaks': 'break',
    'woke': 'wake', 'woken': 'wake', 'waking': 'wake', 'wakes': 'wake',
    'struck': 'strike', 'striking': 'strike', 'strikes': 'strike',
    'fought': 'fight', 'fighting': 'fight', 'fights': 'fight',
    'caught': 'catch', 'catching': 'catch', 'catches': 'catch',
    'taught': 'teach', 'teaching': 'teach', 'teaches': 'teach',
    'bought': 'buy', 'buying': 'buy', 'buys': 'buy',
    'built': 'build', 'building': 'build', 'builds': 'build',
    'dealt': 'deal', 'dealing': 'deal', 'deals': 'deal',
    'fed': 'feed', 'feeding': 'feed', 'feeds': 'feed',
    'led': 'lead', 'leading': 'lead', 'leads': 'lead',
    'lit': 'light', 'lighted': 'light', 'lighting': 'light', 'lights': 'light',
    'shot': 'shoot', 'shooting': 'shoot', 'shoots': 'shoot',
    'sang': 'sing', 'sung': 'sing', 'singing': 'sing', 'sings': 'sing',
    'sank': 'sink', 'sunk': 'sink', 'sinking': 'sink', 'sinks': 'sink',
    'swept': 'sweep', 'sweeping': 'sweep', 'sweeps': 'sweep',
    'tore': 'tear', 'torn': 'tear', 'tearing': 'tear', 'tears': 'tear',
    'wept': 'weep', 'weeping': 'weep', 'weeps': 'weep',
    'wound': 'wind', 'winding': 'wind', 'winds': 'wind',
    'arose': 'arise', 'arisen': 'arise', 'arising': 'arise', 'arises': 'arise',
    'bore': 'bear', 'born': 'bear', 'bearing': 'bear', 'bears': 'bear',
    'forbade': 'forbid', 'forbidden': 'forbid', 'forbidding': 'forbid', 'forbids': 'forbid',
    'overcame': 'overcome', 'overcoming': 'overcome', 'overcomes': 'overcome',
    'withdrew': 'withdraw', 'withdrawn': 'withdraw', 'withdrawing': 'withdraw', 'withdraws': 'withdraw',
    'shook': 'shake', 'shaken': 'shake', 'shaking': 'shake', 'shakes': 'shake',
    'wove': 'weave', 'woven': 'weave', 'weaving': 'weave', 'weaves': 'weave',
    'stuck': 'stick', 'sticking': 'stick', 'sticks': 'stick',
    'swam': 'swim', 'swum': 'swim', 'swimming': 'swim', 'swims': 'swim',
    'swung': 'swing', 'swinging': 'swing', 'swings': 'swing',
    'sought': 'seek', 'seeking': 'seek', 'seeks': 'seek',
    'sent': 'send', 'sending': 'send', 'sends': 'send',
    'lent': 'lend', 'lending': 'lend', 'lends': 'lend',
    'bent': 'bend', 'bending': 'bend', 'bends': 'bend',
    'bound': 'bind', 'binding': 'bind', 'binds': 'bind',
    'bred': 'breed', 'breeding': 'breed', 'breeds': 'breed',
    'bled': 'bleed', 'bleeding': 'bleed', 'bleeds': 'bleed',
    'dug': 'dig', 'digging': 'dig', 'digs': 'dig',
    'spun': 'spin', 'spinning': 'spin', 'spins': 'spin',
    'slid': 'slide', 'sliding': 'slide', 'slides': 'slide',
    'hung': 'hang', 'hanging': 'hang', 'hangs': 'hang',
    'strung': 'string', 'stringing': 'string', 'strings': 'string',
    'ground': 'grind', 'grinding': 'grind', 'grinds': 'grind',
    'beat': 'beat', 'beaten': 'beat', 'beating': 'beat', 'beats': 'beat',
    'lay': 'lie', 'lain': 'lie', 'lying': 'lie', 'lies': 'lie',
    'laid': 'lay', 'laying': 'lay', 'lays': 'lay',
    'split': 'split', 'splitting': 'split', 'splits': 'split',
    'spread': 'spread', 'spreading': 'spread', 'spreads': 'spread',
    'burst': 'burst', 'bursting': 'burst', 'bursts': 'burst',
    'cast': 'cast', 'casting': 'cast', 'casts': 'cast',
    'cost': 'cost', 'costing': 'cost', 'costs': 'cost',
    'hit': 'hit', 'hitting': 'hit', 'hits': 'hit',
    'hurt': 'hurt', 'hurting': 'hurt', 'hurts': 'hurt',
    'put': 'put', 'putting': 'put', 'puts': 'put',
    'set': 'set', 'setting': 'set', 'sets': 'set',
    'shut': 'shut', 'shutting': 'shut', 'shuts': 'shut',
    'bet': 'bet', 'betting': 'bet', 'bets': 'bet',
    'quit': 'quit', 'quitting': 'quit', 'quits': 'quit',
    'upset': 'upset', 'upsetting': 'upset', 'upsets': 'upset',
    'read': 'read', 'reading': 'read', 'reads': 'read',
    'rang': 'ring', 'rung': 'ring', 'ringing': 'ring', 'rings': 'ring',
    'shone': 'shine', 'shining': 'shine', 'shines': 'shine',
    'crept': 'creep', 'creeping': 'creep', 'creeps': 'creep',
    'dreamt': 'dream', 'dreamed': 'dream', 'dreaming': 'dream', 'dreams': 'dream',
    'leapt': 'leap', 'leaped': 'leap', 'leaping': 'leap', 'leaps': 'leap',
    'leant': 'lean', 'leaned': 'lean', 'leaning': 'lean', 'leans': 'lean',
    'learnt': 'learn', 'learned': 'learn', 'learning': 'learn', 'learns': 'learn',
    'smelt': 'smell', 'smelled': 'smell', 'smelling': 'smell', 'smells': 'smell',
    'spelt': 'spell', 'spelled': 'spell', 'spelling': 'spell', 'spells': 'spell',
    'spilt': 'spill', 'spilled': 'spill', 'spilling': 'spill', 'spills': 'spill',
    'spoilt': 'spoil', 'spoiled': 'spoil', 'spoiling': 'spoil', 'spoils': 'spoil',
    'burnt': 'burn', 'burned': 'burn', 'burning': 'burn', 'burns': 'burn',
    'dealt': 'deal', 'dealing': 'deal', 'deals': 'deal',
    'knelt': 'kneel', 'kneeled': 'kneel', 'kneeling': 'kneel', 'kneels': 'kneel',
    'sped': 'speed', 'speeded': 'speed', 'speeding': 'speed', 'speeds': 'speed',
    'spat': 'spit', 'spitting': 'spit', 'spits': 'spit',
    'stung': 'sting', 'stinging': 'sting', 'stings': 'sting',
    'stank': 'stink', 'stunk': 'stink', 'stinking': 'stink', 'stinks': 'stink',
    'swore': 'swear', 'sworn': 'swear', 'swearing': 'swear', 'swears': 'swear',
    'swelled': 'swell', 'swollen': 'swell', 'swelling': 'swell', 'swells': 'swell',
    'tore': 'tear', 'torn': 'tear', 'tearing': 'tear', 'tears': 'tear',
    'wept': 'weep', 'weeping': 'weep', 'weeps': 'weep',
    'wove': 'weave', 'woven': 'weave', 'weaving': 'weave', 'weaves': 'weave',
    'wrung': 'wring', 'wringing': 'wring', 'wrings': 'wring',
    'shrank': 'shrink', 'shrunk': 'shrink', 'shrinking': 'shrink', 'shrinks': 'shrink',
    'forecasts': 'forecast', 'forecasting': 'forecast',
    'broadcasts': 'broadcast', 'broadcasting': 'broadcast',
    'misunderstood': 'misunderstand', 'misunderstanding': 'misunderstand', 'misunderstands': 'misunderstand',
    'overheard': 'overhear', 'overhearing': 'overhear', 'overhears': 'overhear',
    'overpaid': 'overpay', 'overpaying': 'overpay', 'overpays': 'overpay',
    'rebuilt': 'rebuild', 'rebuilding': 'rebuild', 'rebuilds': 'rebuild',
    'underwent': 'undergo', 'undergone': 'undergo', 'undergoing': 'undergo', 'undergoes': 'undergo',
    'undertook': 'undertake', 'undertaken': 'undertake', 'undertaking': 'undertake', 'undertakes': 'undertake',
}

# Words that should NOT have suffixes stripped (common false positives)
NO_STRIP = set("""
this these those there where when why how what which who whom whose
after other another whether either neither either both each every all none
some most few many several much more less least
also however therefore thus moreover meanwhile furthermore nevertheless nonetheless otherwise instead
still already yet ever never always often sometimes usually frequently rarely seldom
now then today tomorrow yesterday soon later recently eventually finally ultimately
something anything everything nothing someone anyone everyone nobody somebody anybody everybody
somewhere anywhere everywhere nowhere
together without within across through along around behind beyond beside near
whether whatever whoever wherever whenever however
already although altogether always among between
""".split())


def lemmatize(word):
    """Conservative rule-based lemmatizer - only strips suffixes when result is a known word."""
    word = word.lower()

    # Check irregular forms first
    if word in IRREGULAR:
        return IRREGULAR[word]

    # Don't strip suffixes from words in NO_STRIP
    if word in NO_STRIP:
        return word

    # Try plural noun endings
    if word.endswith('ies') and len(word) > 4:
        candidate = word[:-3] + 'y'
        if candidate in TEXTBOOK_VOCAB or candidate in IRREGULAR.values():
            return candidate
        # Check if it's a valid word
        return word  # keep as-is if not sure

    if word.endswith('ses') and len(word) > 5:
        candidate = word[:-2]  # analyses -> analysis
        if candidate in TEXTBOOK_VOCAB:
            return candidate

    if word.endswith('ches') or word.endswith('shes') or word.endswith('xes') or word.endswith('oes'):
        if len(word) > 5:
            candidate = word[:-2]
            if candidate in TEXTBOOK_VOCAB:
                return candidate

    if word.endswith('s') and not word.endswith('ss') and not word.endswith('us') and not word.endswith('is') and len(word) > 3:
        candidate = word[:-1]
        if candidate in TEXTBOOK_VOCAB:
            return candidate
        # Don't strip 's' if not sure - keep original

    # Try verb endings
    if word.endswith('ied') and len(word) > 4:
        candidate = word[:-3] + 'y'
        if candidate in TEXTBOOK_VOCAB:
            return candidate

    if word.endswith('ing') and len(word) > 5:
        base = word[:-3]
        # double consonant: running -> run
        if len(base) >= 2 and base[-1] == base[-2] and base[-1] not in 'aeiou':
            candidate = base[:-1]
            if candidate in TEXTBOOK_VOCAB:
                return candidate
        # add 'e': making -> make
        candidate_e = base + 'e'
        if candidate_e in TEXTBOOK_VOCAB:
            return candidate_e
        if base in TEXTBOOK_VOCAB:
            return base
        # keep as-is if not sure

    if word.endswith('ed') and len(word) > 4:
        base = word[:-2]
        # double consonant: stopped -> stop
        if len(base) >= 2 and base[-1] == base[-2] and base[-1] not in 'aeiou':
            candidate = base[:-1]
            if candidate in TEXTBOOK_VOCAB:
                return candidate
        # add 'e': baked -> bake
        candidate_e = base + 'e'
        if candidate_e in TEXTBOOK_VOCAB:
            return candidate_e
        if base in TEXTBOOK_VOCAB:
            return base
        # keep as-is if not sure

    # Adverbs - only strip if base is known
    if word.endswith('ly') and len(word) > 4:
        base = word[:-2]
        if base.endswith('i'):
            candidate = base[:-1] + 'y'  # happily -> happy
            if candidate in TEXTBOOK_VOCAB:
                return candidate
        if base in TEXTBOOK_VOCAB:
            return base
        # keep as-is

    # Comparative/superlative - only strip if base is known
    if word.endswith('iest') and len(word) > 5:
        candidate = word[:-4] + 'y'
        if candidate in TEXTBOOK_VOCAB:
            return candidate

    if word.endswith('ier') and len(word) > 4:
        candidate = word[:-3] + 'y'
        if candidate in TEXTBOOK_VOCAB:
            return candidate

    if word.endswith('est') and len(word) > 5:
        base = word[:-3]
        if len(base) >= 2 and base[-1] == base[-2] and base[-1] not in 'aeiou':
            candidate = base[:-1]
            if candidate in TEXTBOOK_VOCAB:
                return candidate
        candidate_e = base + 'e'
        if candidate_e in TEXTBOOK_VOCAB:
            return candidate_e
        if base in TEXTBOOK_VOCAB:
            return base

    if word.endswith('er') and len(word) > 4:
        base = word[:-2]
        if len(base) >= 2 and base[-1] == base[-2] and base[-1] not in 'aeiou':
            candidate = base[:-1]
            if candidate in TEXTBOOK_VOCAB:
                return candidate
        candidate_e = base + 'e'
        if candidate_e in TEXTBOOK_VOCAB:
            return candidate_e
        if base in TEXTBOOK_VOCAB:
            return base
        # keep as-is if not sure - this is the key fix

    return word


def is_valid_word(word):
    """Check if a word is a valid English word."""
    if len(word) < 3:
        return False
    if not re.match(r'^[a-z]+$', word):
        return False
    # Filter OCR artifacts: 3-5 letter words with no vowels (including y)
    # Valid words like "fly", "gym", "why" have 'y' as vowel
    vowels = set('aeiouy')
    if len(word) <= 5 and not any(c in vowels for c in word):
        return False
    # Filter 3-letter consonant-only clusters (OCR artifacts like "bmd", "srr")
    if len(word) <= 4 and not any(c in vowels for c in word):
        return False
    return True


def process_texts():
    """Process all exam text files and generate word frequency list."""
    exam_dir = '/workspace/output/exam_texts'
    all_text = []

    for fname in sorted(os.listdir(exam_dir)):
        if fname.endswith('.txt'):
            filepath = os.path.join(exam_dir, fname)
            with open(filepath, 'r', encoding='utf-8') as f:
                all_text.append(f.read())

    raw_text = '\n'.join(all_text)

    # Tokenize: extract English words (including contractions)
    tokens = re.findall(r"[A-Za-z]+(?:'[a-z]+)?", raw_text)

    # Process tokens
    word_freq = Counter()
    for token in tokens:
        word = token.lower()

        # Expand contractions
        if word in CONTRACTIONS:
            word = CONTRACTIONS[word]

        # Check stopwords BEFORE lemmatization
        if word in STOPWORDS:
            continue

        # Lemmatize
        lemma = lemmatize(word)

        # Check stopwords AFTER lemmatization
        if lemma in STOPWORDS:
            continue

        # Skip invalid words
        if not is_valid_word(lemma):
            continue

        # Skip textbook vocabulary
        if lemma in TEXTBOOK_VOCAB:
            continue

        # Skip header/metadata words
        if lemma in HEADER_WORDS:
            continue

        # Skip web/OCR artifacts
        if lemma in ARTIFACTS:
            continue

        # Skip proper nouns
        if lemma in PROPER_NOUNS:
            continue

        word_freq[lemma] += 1

    # Filter: keep only freq >= 2 (词频出现2个以上都收录)
    filtered = {w: f for w, f in word_freq.items() if f >= 2}

    # Sort by frequency (desc), then alphabetically
    sorted_words = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))

    return sorted_words, len(tokens), len(word_freq)


if __name__ == '__main__':
    sorted_words, total_tokens, unique_words = process_texts()

    print(f"Total tokens: {total_tokens}")
    print(f"Unique words (before filter): {unique_words}")
    print(f"Words with freq >= 2 (after removing stopwords & textbook vocab): {len(sorted_words)}")
    print(f"\nTop 80 words:")
    for i, (word, freq) in enumerate(sorted_words[:80], 1):
        print(f"  {i}. {word} [{freq}]")

    print(f"\n... words at freq 2:")
    freq2 = [(w, f) for w, f in sorted_words if f == 2]
    for word, freq in freq2[:30]:
        print(f"  {word} [{freq}]")
    print(f"  ... ({len(freq2)} words at freq 2)")

    # Save raw frequency list for review
    with open('/workspace/output/exam_texts/word_freq_raw.txt', 'w', encoding='utf-8') as f:
        for word, freq in sorted_words:
            f.write(f"{word}\t{freq}\n")

    print(f"\nRaw frequency list saved to /workspace/output/exam_texts/word_freq_raw.txt")
