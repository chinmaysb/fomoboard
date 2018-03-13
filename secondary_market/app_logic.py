from secondary_market.models import Transaction, Item, Payment, SendMail, inVenmoHook
import random
from django.shortcuts import render
from django.db.models import Q

def generate_pk():
    letters = list(map(chr, range(65, 91)))
    digits = list(range(0, 9))
    pk_ready = False
    while not pk_ready:
        ret = ""
        ret += ''.join(random.sample(letters, 2))
        ret += ''.join(str(x) for x in random.sample(digits, 2))
        ret += ''.join(random.sample(letters, 1))
        ret += ''.join(str(x) for x in random.sample(digits, 1))
        ret += ''.join(random.sample(letters, 2))

        if not Transaction.objects.filter(pk=ret).count():
            pk_ready = True

    return ret


def dice_coefficient(a, b):
    """dice coefficient 2nt/na + nb."""
    a_bigrams = set(a)
    b_bigrams = set(b)
    overlap = len(a_bigrams & b_bigrams)
    return overlap * 2.0 / (len(a_bigrams) + len(b_bigrams))


def return_icon(description):
    list_of_words = set(description.split())
    list_of_words = list(list_of_words - stop_words)
    dice_high = 0
    for word in list_of_words:
        for icon in fa_dict:
            if (word == icon):
                return fa_dict[icon]
            else:
                dice_new = dice_coefficient(icon, word)
                if (dice_new > dice_high):
                    dice_high = dice_new
                    ret_icon = fa_dict[icon]
    if (dice_high < 0.6):
        return "fa-certificate"
    else:
        return ret_icon.replace("-slash", "")


def similarity(item1, item2):
    item1 = set(item1.description.split()).union(set(item1.name.split()))
    item2 = set(item2.split())
    item1 = list(item1 - stop_words)
    item2 = list(item2 - stop_words)

    dice_high = 0
    for word1 in item1:
        for word2 in item2:
            if (word1 == word2):
                return 1.0
            else:
                dice_new = dice_coefficient(word1, word2)
                if (dice_new > dice_high):
                    dice_high = dice_new

    return dice_high


def createEmail(txn, to, subject, body):
    E = SendMail(txid=txn, to=to, subject=subject, body=body, complete=False)
    try:
        E.save()
        return True
    except Exception as e:
        print(e)
        return False


fa_dict = {'0': 'fa-thermometer-0',
           '1': 'fa-thermometer-1',
           '2': 'fa-thermometer-2',
           '3': 'fa-thermometer-3',
           '4': 'fa-thermometer-4',
           '500px': 'fa-500px',
           'access': 'fa-universal-access',
           'address': 'fa-address-card-o',
           'adjust': 'fa-adjust',
           'adn': 'fa-adn',
           'alien': 'fa-reddit-alien',
           'align': 'fa-align-right',
           'all': 'fa-reply-all',
           'alpha': 'fa-sort-alpha-desc',
           'alt': 'fa-wheelchair-alt',
           'amazon': 'fa-amazon',
           'ambulance': 'fa-ambulance',
           'american': 'fa-american-sign-language-interpreting',
           'amex': 'fa-cc-amex',
           'amount': 'fa-sort-amount-desc',
           'anchor': 'fa-anchor',
           'android': 'fa-android',
           'angellist': 'fa-angellist',
           'angle': 'fa-angle-up',
           'apple': 'fa-apple',
           'archive': 'fa-file-archive-o',
           'area': 'fa-area-chart',
           'arrow': 'fa-long-arrow-up',
           'arrows': 'fa-arrows-alt',
           'asc': 'fa-sort-numeric-asc',
           'asl': 'fa-asl-interpreting',
           'assistive': 'fa-assistive-listening-systems',
           'asterisk': 'fa-asterisk',
           'at': 'fa-at',
           'audio': 'fa-file-audio-o',
           'automobile': 'fa-automobile',
           'awesome': 'fa-fort-awesome',
           'b': 'fa-bluetooth-b',
           'backward': 'fa-step-backward',
           'badge': 'fa-id-badge',
           'bag': 'fa-shopping-bag',
           'balance': 'fa-balance-scale',
           'ball': 'fa-soccer-ball-o',
           'ban': 'fa-ban',
           'bandcamp': 'fa-bandcamp',
           'bank': 'fa-bank',
           'bar': 'fa-bar-chart-o',
           'barcode': 'fa-barcode',
           'bars': 'fa-bars',
           'basket': 'fa-shopping-basket',
           'bath': 'fa-bath',
           'bathtub': 'fa-bathtub',
           'battery': 'fa-battery-three-quarters',
           'bed': 'fa-bed',
           'beer': 'fa-beer',
           'behance': 'fa-behance-square',
           'bell': 'fa-bell-slash-o',
           'bicycle': 'fa-bicycle',
           'binoculars': 'fa-binoculars',
           'birthday': 'fa-birthday-cake',
           'bitbucket': 'fa-bitbucket-square',
           'bitcoin': 'fa-bitcoin',
           'black': 'fa-black-tie',
           'blind': 'fa-blind',
           'bluetooth': 'fa-bluetooth-b',
           'board': 'fa-mortar-board',
           'bold': 'fa-bold',
           'bolt': 'fa-bolt',
           'bomb': 'fa-bomb',
           'book': 'fa-book',
           'bookmark': 'fa-bookmark-o',
           'bouy': 'fa-life-bouy',
           'braille': 'fa-braille',
           'briefcase': 'fa-briefcase',
           'broken': 'fa-chain-broken',
           'brush': 'fa-paint-brush',
           'btc': 'fa-btc',
           'bug': 'fa-bug',
           'building': 'fa-building-o',
           'bullhorn': 'fa-bullhorn',
           'bullseye': 'fa-bullseye',
           'buoy': 'fa-life-buoy',
           'bus': 'fa-bus',
           'buysellads': 'fa-buysellads',
           'cab': 'fa-cab',
           'cake': 'fa-birthday-cake',
           'calculator': 'fa-calculator',
           'calendar': 'fa-calendar-times-o',
           'camera': 'fa-video-camera',
           'camp': 'fa-free-code-camp',
           'cap': 'fa-graduation-cap',
           'car': 'fa-car',
           'card': 'fa-credit-card-alt',
           'caret': 'fa-caret-up',
           'cart': 'fa-shopping-cart',
           'cc': 'fa-cc-visa',
           'cebook': 'fa-facebook-square',
           'center': 'fa-align-center',
           'certificate': 'fa-certificate',
           'chain': 'fa-chain-broken',
           'chart': 'fa-pie-chart',
           'check': 'fa-check-square-o',
           'checkered': 'fa-flag-checkered',
           'chevron': 'fa-chevron-up',
           'child': 'fa-child',
           'chrome': 'fa-chrome',
           'circle': 'fa-stumbleupon-circle',
           'clipboard': 'fa-clipboard',
           'clock': 'fa-clock-o',
           'clone': 'fa-clone',
           'close': 'fa-window-close-o',
           'cloud': 'fa-cloud-upload',
           'club': 'fa-cc-diners-club',
           'cny': 'fa-cny',
           'code': 'fa-free-code-camp',
           'codepen': 'fa-codepen',
           'codiepie': 'fa-codiepie',
           'coffee': 'fa-coffee',
           'cog': 'fa-cog',
           'cogs': 'fa-cogs',
           'columns': 'fa-columns',
           'combinator': 'fa-y-combinator-square',
           'comment': 'fa-comment-o',
           'commenting': 'fa-commenting-o',
           'comments': 'fa-comments-o',
           'commons': 'fa-creative-commons',
           'compass': 'fa-compass',
           'compress': 'fa-compress',
           'connectdevelop': 'fa-connectdevelop',
           'contao': 'fa-contao',
           'control': 'fa-volume-control-phone',
           'copy': 'fa-copy',
           'copyright': 'fa-copyright',
           'creative': 'fa-creative-commons',
           'credit': 'fa-credit-card-alt',
           'crop': 'fa-crop',
           'crosshairs': 'fa-crosshairs',
           'css3': 'fa-css3',
           'cube': 'fa-cube',
           'cubes': 'fa-cubes',
           'cursor': 'fa-i-cursor',
           'cut': 'fa-cut',
           'cutlery': 'fa-cutlery',
           'dashboard': 'fa-dashboard',
           'dashcube': 'fa-dashcube',
           'database': 'fa-database',
           'deaf': 'fa-deaf',
           'deafness': 'fa-deafness',
           'dedent': 'fa-dedent',
           'delicious': 'fa-delicious',
           'desc': 'fa-sort-numeric-desc',
           'description': 'fa-audio-description',
           'desktop': 'fa-desktop',
           'deviantart': 'fa-deviantart',
           'diamond': 'fa-diamond',
           'digg': 'fa-digg',
           'diners': 'fa-cc-diners-club',
           'discover': 'fa-cc-discover',
           'dollar': 'fa-dollar',
           'dot': 'fa-dot-circle-o',
           'double': 'fa-angle-double-up',
           'down': 'fa-toggle-down',
           'download': 'fa-download',
           'dribbble': 'fa-dribbble',
           'drivers': 'fa-drivers-license-o',
           'dropbox': 'fa-dropbox',
           'drupal': 'fa-drupal',
           'edge': 'fa-edge',
           'edit': 'fa-edit',
           'eercast': 'fa-eercast',
           'eject': 'fa-eject',
           'ellipsis': 'fa-ellipsis-v',
           'empire': 'fa-empire',
           'empty': 'fa-thermometer-empty',
           'end': 'fa-hourglass-end',
           'envelope': 'fa-envelope-square',
           'envira': 'fa-envira',
           'eraser': 'fa-eraser',
           'etsy': 'fa-etsy',
           'eur': 'fa-eur',
           'euro': 'fa-euro',
           'excel': 'fa-file-excel-o',
           'exchange': 'fa-stack-exchange',
           'exclamation': 'fa-exclamation-triangle',
           'expand': 'fa-expand',
           'expeditedssl': 'fa-expeditedssl',
           'explorer': 'fa-internet-explorer',
           'external': 'fa-external-link-square',
           'extinguisher': 'fa-fire-extinguisher',
           'eye': 'fa-eye-slash',
           'eyedropper': 'fa-eyedropper',
           'f': 'fa-facebook-f',
           'feed': 'fa-feed',
           'female': 'fa-female',
           'fighter': 'fa-fighter-jet',
           'file': 'fa-file-text-o',
           'files': 'fa-files-o',
           'film': 'fa-film',
           'filter': 'fa-filter',
           'fire': 'fa-fire-extinguisher',
           'firefox': 'fa-firefox',
           'first': 'fa-first-order',
           'flag': 'fa-flag',
           'flash': 'fa-flash',
           'flask': 'fa-flask',
           'flickr': 'fa-flickr',
           'floppy': 'fa-floppy-o',
           'folder': 'fa-folder-open-o',
           'font': 'fa-font-awesome',
           'fonticons': 'fa-fonticons',
           'fork': 'fa-code-fork',
           'fort': 'fa-fort-awesome',
           'forumbee': 'fa-forumbee',
           'forward': 'fa-step-forward',
           'foursquare': 'fa-foursquare',
           'free': 'fa-free-code-camp',
           'frown': 'fa-frown-o',
           'full': 'fa-thermometer-full',
           'futbol': 'fa-futbol-o',
           'g': 'fa-glide-g',
           'gamepad': 'fa-gamepad',
           'gavel': 'fa-gavel',
           'gbp': 'fa-gbp',
           'ge': 'fa-ge',
           'gear': 'fa-gear',
           'gears': 'fa-gears',
           'genderless': 'fa-genderless',
           'get': 'fa-get-pocket',
           'gg': 'fa-gg-circle',
           'ghost': 'fa-snapchat-ghost',
           'gift': 'fa-gift',
           'git': 'fa-git-square',
           'github': 'fa-github-square',
           'gitlab': 'fa-gitlab',
           'gittip': 'fa-gittip',
           'glass': 'fa-glass',
           'glide': 'fa-glide-g',
           'globe': 'fa-globe',
           'google': 'fa-google-wallet',
           'grab': 'fa-hand-grab-o',
           'graduation': 'fa-graduation-cap',
           'gratipay': 'fa-gratipay',
           'grav': 'fa-grav',
           'group': 'fa-object-group',
           'h': 'fa-h-square',
           'hacker': 'fa-hacker-news',
           'half': 'fa-thermometer-half',
           'hand': 'fa-hand-o-up',
           'handshake': 'fa-handshake-o',
           'hard': 'fa-hard-of-hearing',
           'hashtag': 'fa-hashtag',
           'hdd': 'fa-hdd-o',
           'header': 'fa-header',
           'headphones': 'fa-headphones',
           'hearing': 'fa-hard-of-hearing',
           'heart': 'fa-heart-o',
           'heartbeat': 'fa-heartbeat',
           'height': 'fa-text-height',
           'hide': 'fa-times-circle hide',
           'history': 'fa-history',
           'home': 'fa-home',
           'hospital': 'fa-hospital-o',
           'hotel': 'fa-hotel',
           'hourglass': 'fa-hourglass-start',
           'houzz': 'fa-houzz',
           'html5': 'fa-html5',
           'hunt': 'fa-product-hunt',
           'i': 'fa-i-cursor',
           'id': 'fa-id-card-o',
           'ils': 'fa-ils',
           'image': 'fa-file-image-o',
           'imdb': 'fa-imdb',
           'in': 'fa-sign-in',
           'inbox': 'fa-inbox',
           'indent': 'fa-indent',
           'industry': 'fa-industry',
           'info': 'fa-info-circle fa-lg fa-li',
           'inr': 'fa-inr',
           'instagram': 'fa-instagram',
           'institution': 'fa-institution',
           'internet': 'fa-internet-explorer',
           'interpreting': 'fa-asl-interpreting',
           'intersex': 'fa-intersex',
           'ioxhost': 'fa-ioxhost',
           'italic': 'fa-italic',
           'jcb': 'fa-cc-jcb',
           'jet': 'fa-fighter-jet',
           'joomla': 'fa-joomla',
           'jpy': 'fa-jpy',
           'jsfiddle': 'fa-jsfiddle',
           'justify': 'fa-align-justify',
           'key': 'fa-key',
           'keyboard': 'fa-keyboard-o',
           'krw': 'fa-krw',
           'language': 'fa-sign-language',
           'laptop': 'fa-laptop',
           'large': 'fa-th-large',
           'lastfm': 'fa-lastfm-square',
           'leaf': 'fa-leaf',
           'leanpub': 'fa-leanpub',
           'left': 'fa-toggle-left',
           'legal': 'fa-legal',
           'lemon': 'fa-lemon-o',
           'level': 'fa-level-up',
           'lg': 'fa-info-circle fa-lg fa-li',
           'li': 'fa-info-circle fa-lg fa-li',
           'license': 'fa-drivers-license-o',
           'life': 'fa-life-saver',
           'lightbulb': 'fa-lightbulb-o',
           'line': 'fa-line-chart',
           'link': 'fa-link',
           'linkedin': 'fa-linkedin-square',
           'linode': 'fa-linode',
           'linux': 'fa-linux',
           'lira': 'fa-turkish-lira',
           'list': 'fa-th-list',
           'listening': 'fa-assistive-listening-systems',
           'lizard': 'fa-hand-lizard-o',
           'location': 'fa-location-arrow',
           'lock': 'fa-lock',
           'long': 'fa-long-arrow-up',
           'low': 'fa-low-vision',
           'magic': 'fa-magic',
           'magnet': 'fa-magnet',
           'mail': 'fa-mail-reply-all',
           'male': 'fa-male',
           'map': 'fa-map-signs',
           'marker': 'fa-map-marker',
           'mars': 'fa-venus-mars',
           'mastercard': 'fa-cc-mastercard',
           'maxcdn': 'fa-maxcdn',
           'maximize': 'fa-window-maximize',
           'md': 'fa-user-md',
           'meanpath': 'fa-meanpath',
           'medium': 'fa-medium',
           'medkit': 'fa-medkit',
           'meetup': 'fa-meetup',
           'meh': 'fa-meh-o',
           'mercury': 'fa-mercury',
           'microchip': 'fa-microchip',
           'microphone': 'fa-microphone-slash',
           'minimize': 'fa-window-minimize',
           'minus': 'fa-minus-square-o',
           'mixcloud': 'fa-mixcloud',
           'mobile': 'fa-mobile-phone',
           'modx': 'fa-modx',
           'money': 'fa-money',
           'monster': 'fa-optin-monster',
           'moon': 'fa-moon-o',
           'mortar': 'fa-mortar-board',
           'motorcycle': 'fa-motorcycle',
           'mouse': 'fa-mouse-pointer',
           'movie': 'fa-file-movie-o',
           'music': 'fa-music',
           'navicon': 'fa-navicon',
           'neuter': 'fa-neuter',
           'news': 'fa-hacker-news',
           'newspaper': 'fa-newspaper-o',
           'notch': 'fa-circle-o-notch',
           'note': 'fa-sticky-note-o',
           'numeric': 'fa-sort-numeric-desc',
           'o': 'fa-meh-o',
           'object': 'fa-object-ungroup',
           'odnoklassniki': 'fa-odnoklassniki-square',
           'of': 'fa-hard-of-hearing',
           'off': 'fa-volume-off',
           'official': 'fa-google-plus-official',
           'ol': 'fa-list-ol',
           'on': 'fa-toggle-on',
           'open': 'fa-folder-open-o',
           'opencart': 'fa-opencart',
           'openid': 'fa-openid',
           'opera': 'fa-opera',
           'optin': 'fa-optin-monster',
           'order': 'fa-first-order',
           'out': 'fa-sign-out',
           'outdent': 'fa-outdent',
           'overflow': 'fa-stack-overflow',
           'p': 'fa-pinterest-p',
           'pagelines': 'fa-pagelines',
           'paint': 'fa-paint-brush',
           'paper': 'fa-hand-paper-o',
           'paperclip': 'fa-paperclip',
           'paragraph': 'fa-paragraph',
           'paste': 'fa-paste',
           'pause': 'fa-pause-circle-o',
           'paw': 'fa-paw',
           'paypal': 'fa-paypal',
           'pdf': 'fa-file-pdf-o',
           'peace': 'fa-hand-peace-o',
           'pencil': 'fa-pencil-square-o',
           'percent': 'fa-percent',
           'phone': 'fa-volume-control-phone',
           'photo': 'fa-file-photo-o',
           'picture': 'fa-file-picture-o',
           'pie': 'fa-pie-chart',
           'piece': 'fa-puzzle-piece',
           'pied': 'fa-pied-piper-pp',
           'pin': 'fa-map-pin',
           'pinterest': 'fa-pinterest-square',
           'piper': 'fa-pied-piper-pp',
           'plane': 'fa-plane',
           'play': 'fa-youtube-play',
           'plug': 'fa-plug',
           'plus': 'fa-plus-square',
           'pocket': 'fa-get-pocket',
           'podcast': 'fa-podcast',
           'pointer': 'fa-hand-pointer-o',
           'power': 'fa-power-off',
           'powerpoint': 'fa-file-powerpoint-o',
           'pp': 'fa-pied-piper-pp',
           'print': 'fa-print',
           'product': 'fa-product-hunt',
           'puzzle': 'fa-puzzle-piece',
           'qq': 'fa-qq',
           'qrcode': 'fa-qrcode',
           'quarter': 'fa-thermometer-quarter',
           'quarters': 'fa-thermometer-three-quarters',
           'question': 'fa-question-circle-o',
           'quora': 'fa-quora',
           'quote': 'fa-quote-right',
           'ra': 'fa-ra',
           'random': 'fa-random',
           'ravelry': 'fa-ravelry',
           'rebel': 'fa-rebel',
           'rectangle': 'fa-times-rectangle-o',
           'recycle': 'fa-recycle',
           'reddit': 'fa-reddit-square',
           'refresh': 'fa-refresh',
           'registered': 'fa-registered',
           'remove': 'fa-remove',
           'renren': 'fa-renren',
           'reorder': 'fa-reorder',
           'repeat': 'fa-repeat',
           'reply': 'fa-reply-all',
           'resistance': 'fa-resistance',
           'restore': 'fa-window-restore',
           'retro': 'fa-camera-retro',
           'retweet': 'fa-retweet',
           'right': 'fa-toggle-right',
           'ring': 'fa-life-ring',
           'rmb': 'fa-rmb',
           'road': 'fa-road',
           'rock': 'fa-hand-rock-o',
           'rocket': 'fa-rocket',
           'rotate': 'fa-rotate-right',
           'rouble': 'fa-rouble',
           'rss': 'fa-rss-square',
           'rub': 'fa-rub',
           'ruble': 'fa-ruble',
           'rupee': 'fa-rupee',
           's15': 'fa-s15',
           'sari': 'fa-safari',
           'save': 'fa-save',
           'saver': 'fa-life-saver',
           'scale': 'fa-balance-scale',
           'scissors': 'fa-scissors',
           'scribd': 'fa-scribd',
           'search': 'fa-search-plus',
           'secret': 'fa-user-secret',
           'sellsy': 'fa-sellsy',
           'send': 'fa-send-o',
           'server': 'fa-server',
           'share': 'fa-share-alt-square',
           'shekel': 'fa-shekel',
           'sheqel': 'fa-sheqel',
           'shield': 'fa-shield',
           'ship': 'fa-ship',
           'shirtsinbulk': 'fa-shirtsinbulk',
           'shopping': 'fa-shopping-cart',
           'shower': 'fa-shower',
           'shuttle': 'fa-space-shuttle',
           'sign': 'fa-sign-language',
           'signal': 'fa-signal',
           'signing': 'fa-signing',
           'signs': 'fa-map-signs',
           'simplybuilt': 'fa-simplybuilt',
           'sitemap': 'fa-sitemap',
           'skyatlas': 'fa-skyatlas',
           'skype': 'fa-skype',
           'slack': 'fa-slack',
           'slash': 'fa-microphone-slash',
           'sliders': 'fa-sliders',
           'slideshare': 'fa-slideshare',
           'smile': 'fa-smile-o',
           'snapchat': 'fa-snapchat-square',
           'snowflake': 'fa-snowflake-o',
           'soccer': 'fa-soccer-ball-o',
           'sort': 'fa-sort-up',
           'sound': 'fa-file-sound-o',
           'soundcloud': 'fa-soundcloud',
           'space': 'fa-space-shuttle',
           'spinner': 'fa-spinner',
           'spock': 'fa-hand-spock-o',
           'spoon': 'fa-spoon',
           'spotify': 'fa-spotify',
           'square': 'fa-plus-square',
           'st': 'fa-fast-forward',
           'stack': 'fa-stack-overflow',
           'star': 'fa-star-o',
           'start': 'fa-hourglass-start',
           'steam': 'fa-steam-square',
           'step': 'fa-step-forward',
           'stethoscope': 'fa-stethoscope',
           'sticky': 'fa-sticky-note-o',
           'stop': 'fa-stop-circle-o',
           'street': 'fa-street-view',
           'strikethrough': 'fa-strikethrough',
           'stripe': 'fa-cc-stripe',
           'stroke': 'fa-mars-stroke-v',
           'stumbleupon': 'fa-stumbleupon-circle',
           'subscript': 'fa-subscript',
           'subway': 'fa-subway',
           'suitcase': 'fa-suitcase',
           'sun': 'fa-sun-o',
           'superpowers': 'fa-superpowers',
           'superscript': 'fa-superscript',
           'support': 'fa-support',
           'systems': 'fa-assistive-listening-systems',
           'table': 'fa-table',
           'tablet': 'fa-tablet',
           'tachometer': 'fa-tachometer',
           'tack': 'fa-thumb-tack',
           'tag': 'fa-tag',
           'tags': 'fa-tags',
           'tasks': 'fa-tasks',
           'taxi': 'fa-taxi',
           'telegram': 'fa-telegram',
           'television': 'fa-television',
           'tencent': 'fa-tencent-weibo',
           'terminal': 'fa-terminal',
           'text': 'fa-text-width',
           'th': 'fa-th-list',
           'themeisle': 'fa-themeisle',
           'thermometer': 'fa-thermometer-three-quarters',
           'thin': 'fa-circle-thin',
           'three': 'fa-thermometer-three-quarters',
           'thumb': 'fa-thumb-tack',
           'thumbs': 'fa-thumbs-up',
           'ticket': 'fa-ticket',
           'tie': 'fa-black-tie',
           'times': 'fa-times',
           'tint': 'fa-tint',
           'toggle': 'fa-toggle-up',
           'trademark': 'fa-trademark',
           'train': 'fa-train',
           'transgender': 'fa-transgender-alt',
           'trash': 'fa-trash-o',
           'tree': 'fa-tree',
           'trello': 'fa-trello',
           'triangle': 'fa-exclamation-triangle',
           'tripadvisor': 'fa-tripadvisor',
           'trophy': 'fa-trophy',
           'truck': 'fa-truck',
           'try': 'fa-try',
           'tty': 'fa-tty',
           'tumblr': 'fa-tumblr-square',
           'turkish': 'fa-turkish-lira',
           'tv': 'fa-tv',
           'twitch': 'fa-twitch',
           'twitter': 'fa-twitter-square',
           'ul': 'fa-list-ul',
           'umbrella': 'fa-umbrella',
           'underline': 'fa-underline',
           'undo': 'fa-undo',
           'ungroup': 'fa-object-ungroup',
           'universal': 'fa-universal-access',
           'university': 'fa-university',
           'unlink': 'fa-unlink',
           'unlock': 'fa-unlock-alt',
           'unsorted': 'fa-unsorted',
           'up': 'fa-toggle-up',
           'upload': 'fa-upload',
           'usb': 'fa-usb',
           'usd': 'fa-usd',
           'user': 'fa-user-md',
           'users': 'fa-users',
           'v': 'fa-arrows-v',
           'vcard': 'fa-vcard-o',
           'venus': 'fa-venus-mars',
           'viacoin': 'fa-viacoin',
           'viadeo': 'fa-viadeo-square',
           'video': 'fa-file-video-o',
           'view': 'fa-street-view',
           'vimeo': 'fa-vimeo-square',
           'vine': 'fa-vine',
           'visa': 'fa-cc-visa',
           'vision': 'fa-low-vision',
           'vk': 'fa-vk',
           'volume': 'fa-volume-control-phone',
           'w': 'fa-wikipedia-w',
           'wallet': 'fa-google-wallet',
           'warning': 'fa-warning',
           'wechat': 'fa-wechat',
           'weibo': 'fa-weibo',
           'weixin': 'fa-weixin',
           'whatsapp': 'fa-whatsapp',
           'wheelchair': 'fa-wheelchair-alt',
           'width': 'fa-text-width',
           'wifi': 'fa-wifi',
           'wikipedia': 'fa-wikipedia-w',
           'window': 'fa-window-restore',
           'windows': 'fa-windows',
           'won': 'fa-won',
           'word': 'fa-file-word-o',
           'wordpress': 'fa-wordpress',
           'wpbeginner': 'fa-wpbeginner',
           'wpexplorer': 'fa-wpexplorer',
           'wpforms': 'fa-wpforms',
           'wrench': 'fa-wrench',
           'x': 'fa-fax',
           'xing': 'fa-xing-square',
           'y': 'fa-y-combinator-square',
           'yahoo': 'fa-yahoo',
           'yc': 'fa-yc-square',
           'yelp': 'fa-yelp',
           'yen': 'fa-yen',
           'yoast': 'fa-yoast',
           'youtube': 'fa-youtube-square',
           'zip': 'fa-file-zip-o'}
stop_words = set(["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"])


def dispatcher(buy_or_sell, request):
    context = dict()
    transactions = []
    item = Item.objects.get(id=request.POST['item'])
    if (buy_or_sell == "sell"):
        txset = Transaction.objects.filter(Q(item=item) & Q(seller=None)).order_by('exec_price', '-tstamp')
        context['context'] = "Sell"
        context['handler_url'] = "dosell"

    else:
        txset = Transaction.objects.filter(Q(item=item) & Q(buyer=None)).order_by('exec_price', '-tstamp')
        context['context'] = "Buy"
        context['handler_url'] = "dobuy"

    context['name'] = item.name
    context['description'] = item.description
    context['icon'] = item.icon

    for transaction in txset:
        q = dict()
        try:
            q['buypx'] = transaction.exec_price  # spread always paid by the seller
            q['id'] = transaction.id
            q['quantity'] = transaction.quantity
            q['pickup_location'] = transaction.pickup_location
            q['total_price'] = transaction.total_price
            transactions.append(q)
        except:
            pass

    context['transactions'] = transactions
    context['client_ip'] = request.META['REMOTE_ADDR']
    return render(request, 'dispatcher.html', context)


def offerdispatcher(buy_or_sell, request):
    context = dict()
    item = Transaction.objects.get(id=request.POST['item']).item
    transaction = Transaction.objects.get(id=request.POST['item'])
    context['handler_url'] = "executetransaction"
    if (buy_or_sell == "sell"):
        context['context'] = "Sell"
    else:
        context['context'] = "Buy"

    context['name'] = item.name
    context['description'] = item.description
    context['icon'] = item.icon
    context['face_value'] = item.face_value
    context['exec_price'] = transaction.exec_price  # spread always paid by the seller
    context['id'] = transaction.id
    context['quantity'] = transaction.quantity
    context['pickup_location'] = transaction.pickup_location
    context['total_price'] = transaction.total_price
    context['client_ip'] = request.META['REMOTE_ADDR']
    return render(request, 'offer.html', context)


def verifypayment(request):
    # Payment.objects.all().delete()
    context = dict()

    payload = request.body.decode('utf-8')
    P = Payment(json_text="Body: " + str(payload) + ">>>>>>")
    P.save()

    payload = request.META['REMOTE_ADDR']
    P = Payment(json_text="Meta: " + str(payload) + ">>>>>>>")
    P.save()

    context['pmts'] = Payment.objects.all()
    return render(request, 'verifypayment.html', context)
