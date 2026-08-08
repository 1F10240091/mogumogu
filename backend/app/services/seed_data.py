"""レシピマスタのシードデータ。

保育園の夕食で定番の料理レシピ。レシピ名・使用食品・作り方をセットで管理する。
使用食品（ingredients）はアレルゲン判定と買い物リスト集計に使われる。

実在レシピ（cookpad 国立市公式キッチン・kurachiru 等の公的な幼児食/離乳食レシピ）を
参考に、園児向けの分量に調整して収録している。
"""

SEED_RECIPES: list[dict] = [
    # --- 主菜（やわらか・低塩の幼児食） ---
    {
        "name": "タラじゃがバーグ",
        "meal_type": "main",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "たらの切り身", "quantity": "60", "unit": "g"},
            {"name": "じゃがいも", "quantity": "100", "unit": "g"},
            {"name": "玉ねぎ", "quantity": "30", "unit": "g"},
            {"name": "片栗粉", "quantity": "小さじ", "unit": "1"},
            {"name": "ケチャップ", "quantity": "小さじ", "unit": "1"},
            {"name": "サラダ油", "quantity": "小さじ", "unit": "1"},
            {"name": "水", "quantity": "大さじ", "unit": "2"},
        ],
        "instructions": (
            "1. じゃがいもは一口大、玉ねぎはみじん切りにする。\n"
            "2. じゃがいもと玉ねぎを耐熱皿で電子レンジ加熱し、じゃがいもを粗くつぶす。\n"
            "3. たこに片栗粉をまぶして水を加え、レンジで加熱して粗くほぐす。\n"
            "4. じゃがいも・たこ・ケチャップを混ぜて小判型にし、フライパンで両面を焼く。"
        ),
    },
    {
        "name": "豚ひき肉とさつまいもの炒め煮",
        "meal_type": "main",
        "cook_time_minutes": 10,
        "ingredients": [
            {"name": "豚ひき肉", "quantity": "60", "unit": "g"},
            {"name": "さつまいも", "quantity": "80", "unit": "g"},
            {"name": "大根", "quantity": "40", "unit": "g"},
            {"name": "だし", "quantity": "100", "unit": "ml"},
            {"name": "こいしょうゆ", "quantity": "少々", "unit": ""},
            {"name": "サラダ油", "quantity": "小さじ", "unit": "1"},
        ],
        "instructions": (
            "1. さつまいもと大根は1cm角に切る。さつまいもは水にさらす。\n"
            "2. 豚ひき肉は湯通しして余分な脂を落とす。\n"
            "3. フライパンで野菜を炒め、ひき肉・だしを加えて蓋をして柔らかく煮る。\n"
            "4. しょうゆを少々加え、さつまいもが柔らかくなったら火を止める。"
        ),
    },
    {
        "name": "鶏ひき肉のキャベツ団子",
        "meal_type": "main",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "鶏ひき肉", "quantity": "80", "unit": "g"},
            {"name": "キャベツ", "quantity": "50", "unit": "g"},
            {"name": "にんじん", "quantity": "30", "unit": "g"},
            {"name": "片栗粉", "quantity": "小さじ", "unit": "1"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1/2"},
            {"name": "だし", "quantity": "200", "unit": "ml"},
        ],
        "instructions": (
            "1. キャベツとにんじんはみじん切りにする。\n"
            "2. 鶏ひき肉・野菜・片栗粉・しょうゆを混ぜて小判形に成形する。\n"
            "3. だしを沸かして入れ、蓋をして15分ほど煮込む。"
        ),
    },
    {
        "name": "大豆入りポークチャップ",
        "meal_type": "main",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "豚ひき肉", "quantity": "60", "unit": "g"},
            {"name": "玉ねぎ", "quantity": "30", "unit": "g"},
            {"name": "大豆水煮", "quantity": "30", "unit": "g"},
            {"name": "野菜スープ", "quantity": "100", "unit": "ml"},
            {"name": "ケチャップ", "quantity": "小さじ", "unit": "1"},
            {"name": "砂糖", "quantity": "小さじ", "unit": "1/2"},
            {"name": "片栗粉", "quantity": "小さじ", "unit": "1/2"},
            {"name": "サラダ油", "quantity": "小さじ", "unit": "1"},
        ],
        "instructions": (
            "1. 玉ねぎを1cm角に切る。大豆は半分に切る。\n"
            "2. フライパンで玉ねぎとひき肉を炒め、スープを加えて蓋をし5分煮る。\n"
            "3. 大豆が柔らかくなり煮汁が半量になるまで煮たら、ケチャップ・砂糖で味付けする。\n"
            "4. 水溶き片栗粉でとろうをつける。"
        ),
    },
    {
        "name": "豚肉とキャベツの味噌炒め",
        "meal_type": "main",
        "cook_time_minutes": 15,
        "ingredients": [
            {"name": "豚小間切れ肉", "quantity": "100", "unit": "g"},
            {"name": "キャベツ", "quantity": "1/4", "unit": "玉"},
            {"name": "ごま油", "quantity": "小さじ", "unit": "2"},
            {"name": "味噌", "quantity": "大さじ", "unit": "1"},
            {"name": "砂糖", "quantity": "小さじ", "unit": "2"},
            {"name": "みりん", "quantity": "小さじ", "unit": "2"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1"},
        ],
        "instructions": (
            "1. キャベツを2cm角に切って洗い、水気を切る。\n"
            "2. 味噌・みりん・砂糖・しょうゆを混ぜ合わせる。\n"
            "3. フライパンにごま油を熱し豚肉を炒める。\n"
            "4. 火が通ったらキャベツを加え、しんなりしたら調味料を絡める。"
        ),
    },
    {
        "name": "ビビンバ丼",
        "meal_type": "main",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "ごはん", "quantity": "1", "unit": "膳分"},
            {"name": "豚ひき肉", "quantity": "120", "unit": "g"},
            {"name": "おろしにんにく", "quantity": "少々", "unit": ""},
            {"name": "おろししょうが", "quantity": "少々", "unit": ""},
            {"name": "砂糖", "quantity": "小さじ", "unit": "1"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1"},
            {"name": "もやし", "quantity": "80", "unit": "g"},
            {"name": "にんじん", "quantity": "30", "unit": "g"},
            {"name": "ほうれん草", "quantity": "60", "unit": "g"},
            {"name": "ごま油", "quantity": "小さじ", "unit": "2"},
        ],
        "instructions": (
            "1. 豚ひき肉をにんにく・しょうが・砂糖・しょうゆで下味をつける。\n"
            "2. もやしを短く切る。にんじん・ほうれん草はやわらかくゆで細かく切る。\n"
            "3. ひき肉をごま油で炒め、色が変わったら野菜を加えて炒める。\n"
            "4. ごはんにのせて完成。"
        ),
    },
    {
        "name": "鶏胸肉のカレー風味",
        "meal_type": "main",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "鶏胸肉", "quantity": "150", "unit": "g"},
            {"name": "酒", "quantity": "大さじ", "unit": "1"},
            {"name": "カレーパウダー", "quantity": "小さじ", "unit": "1/3"},
            {"name": "砂糖", "quantity": "小さじ", "unit": "1"},
            {"name": "ソース", "quantity": "小さじ", "unit": "1"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1"},
            {"name": "ケチャップ", "quantity": "小さじ", "unit": "1"},
            {"name": "片栗粉", "quantity": "大さじ", "unit": "1"},
            {"name": "サラダ油", "quantity": "大さじ", "unit": "2"},
        ],
        "instructions": (
            "1. 鶏胸肉を2cm角に切り、酒と塩を揉み込む。\n"
            "2. カレーパウダー・砂糖・ソース・しょうゆ・ケチャップ・水を混ぜておく。\n"
            "3. 鶏肉に片栗粉をまぶし、フライパンの油で炒めて火を通す。\n"
            "4. 余分な油をふき取り、調味料を加えてとろみがつくまで絡める。"
        ),
    },
    {
        "name": "ふんわり鶏つくね（甘辛だれ）",
        "meal_type": "main",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "鶏ひき肉", "quantity": "120", "unit": "g"},
            {"name": "木綿豆腐", "quantity": "1/6", "unit": "丁"},
            {"name": "にんじん", "quantity": "20", "unit": "g"},
            {"name": "片栗粉", "quantity": "小さじ", "unit": "1"},
            {"name": "だし", "quantity": "100", "unit": "ml"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1"},
            {"name": "砂糖", "quantity": "小さじ", "unit": "1/4"},
        ],
        "instructions": (
            "1. 豆腐を水切りして崩し、にんじんをすりおろす。\n"
            "2. 鶏ひき肉・豆腐・にんじん・片栗粉を混ぜ、つくねに丸める。\n"
            "3. フライパンで焼き色をつけ、だし・しょうゆ・砂糖で甘辛く絡める。"
        ),
    },
    {
        "name": "やわらか鶏ひき肉ハンバーグ",
        "meal_type": "main",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "鶏ひき肉", "quantity": "150", "unit": "g"},
            {"name": "玉ねぎ", "quantity": "みじん切り", "unit": "1/4"},
            {"name": "パン粉", "quantity": "大さじ", "unit": "2"},
            {"name": "牛乳", "quantity": "大さじ", "unit": "2"},
            {"name": "卵", "quantity": "1/2", "unit": "個"},
            {"name": "ケチャップ", "quantity": "小さじ", "unit": "1"},
        ],
        "instructions": (
            "1. 玉ねぎをみじん切りにして、しんなりするまで加熱して冷ます。\n"
            "2. 鶏ひき肉・パン粉・牛乳・卵を混ぜて成形する。\n"
            "3. フライパンで両面を焼き、水を少し加えて蓋をし弱火で蒸し焼きにする。"
        ),
    },
    {
        "name": "鶏だんごの甘酢あん",
        "meal_type": "main",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "鶏ひき肉", "quantity": "150", "unit": "g"},
            {"name": "玉ねぎ", "quantity": "1/4", "unit": "個"},
            {"name": "片栗粉", "quantity": "小さじ", "unit": "2"},
            {"name": "トマトケチャップ", "quantity": "小さじ", "unit": "1"},
            {"name": "砂糖", "quantity": "小さじ", "unit": "1/2"},
        ],
        "instructions": (
            "1. 玉ねぎをみじん切りにし、鶏ひき肉に片栗粉と混ぜて小さなだんごを作る。\n"
            "2. だんごをゆでて浮き上がったら取り出す。\n"
            "3. ケチャップ・砂糖を煮立て、だんごを加えて絡める。"
        ),
    },
    {
        "name": "さばと小松菜のふわふわれんざ",
        "meal_type": "main",
        "cook_time_minutes": 15,
        "ingredients": [
            {"name": "さけ", "quantity": "60", "unit": "g"},
            {"name": "小松菜", "quantity": "1/4", "unit": "束"},
            {"name": "鶏ひき肉", "quantity": "80", "unit": "g"},
            {"name": "だし", "quantity": "150", "unit": "ml"},
            {"name": "片栗粉", "quantity": "小さじ", "unit": "1"},
        ],
        "instructions": (
            "1. さけはゆでて骨を除き、ほぐす。小松菜はやわらかく茹でて刻む。\n"
            "2. 鶏ひき肉を混ぜて成形し、だしで煮る。\n"
            "3. とろみ用の片栗粉でやわらかく仕上げる。\n"
            "4. 一部のディッシュに合わせやすいよう、ごはんと一緒に出してもよい。"
        ),
    },
    {
        "name": "鶏ささみのとろとろチーズスティック",
        "meal_type": "main",
        "cook_time_minutes": 15,
        "ingredients": [
            {"name": "鶏ささみ", "quantity": "80", "unit": "g"},
            {"name": "片栗粉", "quantity": "大さじ", "unit": "1"},
            {"name": "パン粉", "quantity": "大さじ", "unit": "3"},
            {"name": "粉チーズ", "quantity": "大さじ", "unit": "1"},
            {"name": "水", "quantity": "大さじ", "unit": "1"},
            {"name": "サラダ油", "quantity": "大さじ", "unit": "2"},
        ],
        "instructions": (
            "1. 鶏ささみを一口大に切り、片栗粉・水を絡める。\n"
            "2. パン粉と粉チーズを混ぜて衣をつける。\n"
            "3. フライパンで両面を焼き、火が通ったら完成。"
        ),
    },
    {
        "name": "かぼちゃコロッケ",
        "meal_type": "main",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "かぼちゃ", "quantity": "150", "unit": "g"},
            {"name": "豚ひき肉", "quantity": "40", "unit": "g"},
            {"name": "玉ねぎ", "quantity": "30", "unit": "g"},
            {"name": "パン粉", "quantity": "大さじ", "unit": "3"},
            {"name": "小麦粉", "quantity": "大さじ", "unit": "2"},
            {"name": "卵", "quantity": "1/2", "unit": "個"},
            {"name": "サラダ油", "quantity": "大さじ", "unit": "2"},
        ],
        "instructions": (
            "1. かぼちゃを柔らかく蒸してつぶす。\n"
            "2. 玉ねぎとひき肉を炒めてかぼちゃに混ぜる。\n"
            "3. 形を作って小麦粉・卵・パン粉をつけ、揚げ焼きにする。"
        ),
    },
    # --- 汁物（やさしい味） ---
    {
        "name": "みそ汁",
        "meal_type": "soup",
        "cook_time_minutes": 10,
        "ingredients": [
            {"name": "玉ねぎ", "quantity": "1/8", "unit": "個"},
            {"name": "わかめ", "quantity": "少々", "unit": ""},
            {"name": "みそ", "quantity": "小さじ", "unit": "1"},
            {"name": "だし", "quantity": "150", "unit": "ml"},
        ],
        "instructions": (
            "1. 玉ねぎを薄切りにしてだしで柔らかく煮る。\n"
            "2. わかめを加えてひと煮立ちさせる。\n"
            "3. 一度火を離してみそを溶き入れる。"
        ),
    },
    {
        "name": "野菜と鶏だんごのスープ",
        "meal_type": "soup",
        "cook_time_minutes": 15,
        "ingredients": [
            {"name": "鶏ひき肉", "quantity": "50", "unit": "g"},
            {"name": "にんじん", "quantity": "30", "unit": "g"},
            {"name": "玉ねぎ", "quantity": "30", "unit": "g"},
            {"name": "キャベツ", "quantity": "30", "unit": "g"},
            {"name": "だし", "quantity": "200", "unit": "ml"},
            {"name": "片栗粉", "quantity": "小さじ", "unit": "1/2"},
        ],
        "instructions": (
            "1. 鶏ひき肉に片栗粉を加えて小さなだんごにする。\n"
            "2. 野菜を細かく切り、だしでやわらか煮る。\n"
            "3. だんごを入れて火が通るまで煮る。"
        ),
    },
    {
        "name": "野菜のトマトミルクスープ",
        "meal_type": "soup",
        "cook_time_minutes": 15,
        "ingredients": [
            {"name": "じゃがいも", "quantity": "40", "unit": "g"},
            {"name": "玉ねぎ", "quantity": "1/8", "unit": "個"},
            {"name": "トマト", "quantity": "1/4", "unit": "個"},
            {"name": "牛乳", "quantity": "150", "unit": "ml"},
            {"name": "水", "quantity": "100", "unit": "ml"},
        ],
        "instructions": (
            "1. 野菜をみじん切りにする。\n"
            "2. 水で野菜を柔らかく煮る。\n"
            "3. 牛乳を加えて温め、とろみが出るまで煮る。"
        ),
    },
    {
        "name": "豆腐とひき肉のふんわりスープ",
        "meal_type": "soup",
        "cook_time_minutes": 15,
        "ingredients": [
            {"name": "木綿豆腐", "quantity": "1/6", "unit": "丁"},
            {"name": "豚ひき肉", "quantity": "40", "unit": "g"},
            {"name": "にんじん", "quantity": "30", "unit": "g"},
            {"name": "だし", "quantity": "150", "unit": "ml"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1/2"},
            {"name": "片栗粉", "quantity": "小さじ", "unit": "1/2"},
        ],
        "instructions": (
            "1. 豆腐・にんじんを小さく切る。\n"
            "2. 豚ひき肉をだしでほぐしながら煮る。\n"
            "3. 豆腐・にんじんを加えて柔らかく煮、とろみをつける。"
        ),
    },
    {
        "name": "野菜スープ",
        "meal_type": "soup",
        "cook_time_minutes": 15,
        "ingredients": [
            {"name": "にんじん", "quantity": "1/4", "unit": "本"},
            {"name": "玉ねぎ", "quantity": "1/8", "unit": "個"},
            {"name": "キャベツ", "quantity": "1", "unit": "枚"},
            {"name": "だし", "quantity": "150", "unit": "ml"},
        ],
        "instructions": "1. 野菜を細かく切る。\n2. だしで野菜を柔らかく煮る。",
    },
    # --- 副菜（やさしい加熱・とろみ） ---
    {
        "name": "じゃがいもとにんじんのきんぴら",
        "meal_type": "side",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "じゃがいも", "quantity": "100", "unit": "g"},
            {"name": "にんじん", "quantity": "40", "unit": "g"},
            {"name": "砂糖", "quantity": "小さじ", "unit": "1"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1"},
            {"name": "白すりごま", "quantity": "小さじ", "unit": "1/2"},
            {"name": "サラダ油", "quantity": "小さじ", "unit": "1/2"},
        ],
        "instructions": (
            "1. じゃがいもとにんじんは細めの短冊に切る。\n"
            "2. フライパンで炒め、砂糖・しょうゆ・水を加えて炒め煮にする。\n"
            "3. すりごまをふりかける。"
        ),
    },
    {
        "name": "豆腐のごま和え",
        "meal_type": "side",
        "cook_time_minutes": 15,
        "ingredients": [
            {"name": "絹ごし豆腐", "quantity": "1/4", "unit": "丁"},
            {"name": "ほうれん草", "quantity": "50", "unit": "g"},
            {"name": "白すりごま", "quantity": "小さじ", "unit": "1"},
            {"name": "砂糖", "quantity": "小さじ", "unit": "1/2"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1/2"},
            {"name": "マヨネーズ", "quantity": "小さじ", "unit": "1"},
        ],
        "instructions": (
            "1. ほうれん草をゆでて水気を絞り、細かく切る。\n"
            "2. 豆腐を水切りし、すりごま・砂糖・しょうゆ・マヨネーズを混ぜる。\n"
            "3. ほうれん草と豆腐を和える。"
        ),
    },
    {
        "name": "ほうれん草の納豆和え",
        "meal_type": "side",
        "cook_time_minutes": 10,
        "ingredients": [
            {"name": "ほうれん草", "quantity": "100", "unit": "g"},
            {"name": "にんじん", "quantity": "30", "unit": "g"},
            {"name": "ひきわり納豆", "quantity": "1", "unit": "パック"},
            {"name": "削り節", "quantity": "大さじ", "unit": "1"},
        ],
        "instructions": (
            "1. ほうれん草は2〜3cmに切ってゆでる。にんじんは千切りにしてやわらかくゆでる。\n"
            "2. ゆでた野菜とひき納豆・削り節を混ぜ合わせる。"
        ),
    },
    {
        "name": "南瓜とチーズのサラダ",
        "meal_type": "side",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "かぼちゃ", "quantity": "150", "unit": "g"},
            {"name": "きゅうり", "quantity": "1/2", "unit": "本"},
            {"name": "にんじん", "quantity": "60", "unit": "g"},
            {"name": "チーズ", "quantity": "20", "unit": "g"},
            {"name": "マヨネーズ", "quantity": "大さじ", "unit": "1"},
            {"name": "砂糖", "quantity": "小さじ", "unit": "1"},
        ],
        "instructions": (
            "1. かぼちゃは皮をむき2cm角へ、きゅうりは半月切り、にんじんはいちょう切りにする。\n"
            "2. かぼちゃとにんじんを電子レンジで加熱して粗くつぶす。\n"
            "3. 温かいうちにチーズを溶かし、粗熱が取れたらきゅうり・砂糖・マヨを和える。"
        ),
    },
    {
        "name": "小松菜と油揚げのお浸し",
        "meal_type": "side",
        "cook_time_minutes": 10,
        "ingredients": [
            {"name": "小松菜", "quantity": "100", "unit": "g"},
            {"name": "油揚げ", "quantity": "1/4", "unit": "枚"},
            {"name": "しらす干し", "quantity": "小さじ", "unit": "2"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1/2"},
        ],
        "instructions": (
            "1. 小松菜をゆでて水気を絞り、3cmに切る。\n"
            "2. 油揚げを熱湯で油抜きして薄切りにする。\n"
            "3. 小松菜・油揚げ・しらすをしょうゆで和える。"
        ),
    },
    {
        "name": "キャベツのおかか塩和え",
        "meal_type": "side",
        "cook_time_minutes": 5,
        "ingredients": [
            {"name": "キャベツ", "quantity": "1/4", "unit": "玉"},
            {"name": "かつおぶし", "quantity": "1/2", "unit": "パック"},
            {"name": "塩", "quantity": "少々", "unit": ""},
        ],
        "instructions": (
            "1. キャベツを細切りにしてゆであげる。\n"
            "2. 水気を絞って塩で和える。\n"
            "3. かつおぶしを混ぜる。"
        ),
    },
    {
        "name": "胡瓜とささみのごま酢あえ",
        "meal_type": "side",
        "cook_time_minutes": 15,
        "ingredients": [
            {"name": "鶏ささみ", "quantity": "60", "unit": "g"},
            {"name": "きゅうり", "quantity": "1/2", "unit": "本"},
            {"name": "白すりごま", "quantity": "小さじ", "unit": "1"},
            {"name": "砂糖", "quantity": "小さじ", "unit": "1/2"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1/2"},
            {"name": "酢", "quantity": "小さじ", "unit": "1/2"},
        ],
        "instructions": (
            "1. 鶏ささみをゆでて細かくさく。きゅうりは薄切りして塩もみする。\n"
            "2. すりごま・砂糖・しょうゆ・酢を混ぜてドレを作る。\n"
            "3. ささみときゅうりをドレで和える。"
        ),
    },
    {
        "name": "れんこんと大根のやわらか煮",
        "meal_type": "side",
        "cook_time_minutes": 20,
        "ingredients": [
            {"name": "大根", "quantity": "2", "unit": "cm"},
            {"name": "れんこん", "quantity": "30", "unit": "g"},
            {"name": "鶏ひき肉", "quantity": "40", "unit": "g"},
            {"name": "だし", "quantity": "150", "unit": "ml"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1"},
        ],
        "instructions": (
            "1. 大根・れんこんを薄めに切り、下ゆでする。\n"
            "2. 鶏ひきと一緒にだしで煮る。\n"
            "3. しょうゆで薄味にし、とろりと柔らかく仕上げる。"
        ),
    },
    {
        "name": "ブロッコリーのやわらかマッシュ",
        "meal_type": "side",
        "cook_time_minutes": 15,
        "ingredients": [
            {"name": "ブロッコリー", "quantity": "小房", "unit": "3"},
            {"name": "じゃがいも", "quantity": "1", "unit": "個"},
            {"name": "牛乳", "quantity": "大さじ", "unit": "2"},
        ],
        "instructions": (
            "1. ブロッコリーとじゃがいを柔らかくゆでる。\n"
            "2. 粗つぶしにして牛乳を混ぜてなめらかにする。"
        ),
    },
    {
        "name": "かぼちゃのとろみ煮",
        "meal_type": "side",
        "cook_time_minutes": 15,
        "ingredients": [
            {"name": "かぼちゃ", "quantity": "60", "unit": "g"},
            {"name": "玉ねぎ", "quantity": "20", "unit": "g"},
            {"name": "だし", "quantity": "100", "unit": "ml"},
            {"name": "しょうゆ", "quantity": "小さじ", "unit": "1/2"},
            {"name": "片栗粉", "quantity": "小さじ", "unit": "1/2"},
        ],
        "instructions": (
            "1. かぼちゃと玉ねぎを細かく切る。\n"
            "2. だしで柔らかく煮る。\n"
            "3. しょうゆで味付けし、水溶か片栗でとろみをつける。"
        ),
    },
    # --- 主食 ---
    {
        "name": "ごはん",
        "meal_type": "staple",
        "cook_time_minutes": 30,
        "ingredients": [{"name": "米", "quantity": "1", "unit": "合"}],
        "instructions": "炊飯器で炊いて、やわらかめに炊く。",
    },
]