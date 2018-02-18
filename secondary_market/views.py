from secondary_market.mailsender import send_mail
from django.shortcuts import render
from secondary_market.models import Transaction, Item
from django.db.models import Count, Min, Sum, Avg
from django.db.models import Q
# from secondary_market import app_logic
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
import venmo as vm
import random
import pickle

def home(request, context=dict()):
    items_for_sale = []

    for item in Item.objects.all():
        if len(item.transaction_set.filter(Q(buyer=None)))>0:
            q = dict()
            q['name'] = item.name
            q['description'] = item.description
            q['buypx'] = item.transaction_set.filter(Q(buyer=None)).aggregate(Min('exp_price'))['exp_price__min']
            q['txid'] = item.transaction_set.filter(Q(buyer=None) & Q(exp_price=q['buypx'])).order_by("-id")[0].id
            # Add $1 spread
            q['buypx'] +=1
            items_for_sale.append(q)

    context['items_for_sale']= items_for_sale
    context['client_ip'] = request.META['REMOTE_ADDR']
    return render(request, 'index.html', context)

def dosellitem(request):
    context = dict()
    try:
        new_name = request.POST["name"]
        new_description= request.POST["description"]
        new_face_value= request.POST["face_value"]
        new_expiry_date= request.POST["expiry_date"]
        I = Item(name=new_name, description=new_description, face_value=new_face_value, expiry_date=new_expiry_date)
        I.save()
        new_seller = request.POST['seller']
        new_seller_venmo_handle = request.POST['seller_venmo_handle']
        new_exp_price = request.POST['exp_price']
        T = Transaction(item=I, seller=new_seller, seller_venmo_handle=new_seller_venmo_handle,
                        exp_price=new_exp_price)
        T.save()
        context['TransactionSuccess'] = True
        context[
            'TransactionMessage'] = "You have successfully listed an item for sale! Please note down your transaction ID: " + str(T.id) + ".We will let you know once someone has purchased this item. This note has also been emailed to you."
        send_mail(new_seller, "CBS Secondary Market Transaction", context['TransactionMessage'])
        return home(request, context)
    except:
        context['TransactionSuccess'] = False
        context[
            'TransactionMessage'] = "Sorry, that did not work - please try again!"
        return render(request, 'sell.html', context)


def doselloffer(request):
    context = dict()
    try:
        new_item = Item.objects.get(id=request.POST['offereditem'])
        new_seller = request.POST['seller']
        new_seller_venmo_handle = request.POST['seller_venmo_handle']
        new_exp_price = request.POST['exp_price']

        T = Transaction(item=new_item, seller=new_seller,seller_venmo_handle=new_seller_venmo_handle, exp_price=new_exp_price)
        T.save()
        context['TransactionSuccess'] = True
        context[
            'TransactionMessage'] = "You have successfully listed an item for sale! Please note down your transaction ID: " + str(T.id) + ".<br>We will let you know once someone has purchased this item. This note has also been emailed to you."
        send_mail(new_seller, "CBS Secondary Market Transaction", context['TransactionMessage'])
        return home(request, context)
    except:
        context['TransactionSuccess'] = False
        context[
            'TransactionMessage'] = "Sorry, that did not work - please try again!"
        return render(request, 'sell.html', context)

def dobuyitem(request):
    context = dict()
    txID = request.POST['txID']
    new_buyer =  request.POST["buyer"]
    new_buyer_venmo_handle = request.POST["buyer_venmo_handle"]
    try:
        T = Transaction.objects.get(id=txID)
        T.buyer = new_buyer
        T.buyer_venmo_handle = new_buyer_venmo_handle
        T.save()
        context['TransactionSuccess'] = True
        context['TransactionMessage'] = "You have successfully bought the item! Please note down your transaction ID: " + str(txID) + ". Please get in touch with the seller at " + T.seller + " . We won't release payment to him/her for the next 24 hours, so please report to us if you have trouble completing the transaction, and we will refund you. This note has also been emailed to you."
        send_mail(new_buyer, "CBS Secondary Market Transaction", context['TransactionMessage'])
        send_mail(T.seller, "CBS Secondary Market Transaction", "Your item has been sold! Please get in touch with " +new_buyer +" to complete the transaction. You will receive the funds in your Venmo account in 24 hours. Transaction ID: " + str(txID) +"." )
        vm.payment.charge('@'+new_buyer_venmo_handle.replace("@", ""), random.random(), "CBS Secondary Market Transaction ID" + str(txID))
        vm.payment.pay('@'+T.seller_venmo_handle.replace("@", ""), random.random(), "CBS Secondary Market Transaction ID" + str(txID))
        return home(request, context)
    except:
        context['TransactionSuccess'] = False
        context[
            'TransactionMessage'] = "That purchase didn't work! The item you were looking for may have been purchased by someone else. Please try again!"
        return home(request, context)

def dobuy(request):
    context = dict()
    context['item_to_buy'] = Transaction.objects.get(id=request.POST["buyitem"]).item
    context['transaction'] = Transaction.objects.get(id=request.POST["buyitem"])
    # Add spread here
    context['transaction'].exp_price +=1
    return render(request, 'buy.html', context)

def sell(request):
    context = dict()
    context['items_for_sale'] = Item.objects.all()
    return render(request, 'sell.html', context)

def verifypayment(request):
    context = dict()
    if(request.method=='GET'):
        context['t'] = str(request.GET)
        output = open('output.txt', 'a')
        output.write("Here I am")
        output.write(str(request.GET))
        output.close()
    else:
        context['t'] = str(request.POST)
        output = open('output.txt', 'a')
        output.write("Here I am")
        output.write(str(request.POST))
        output.close()
    return render(request, 'verifypayment.html', context)

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
