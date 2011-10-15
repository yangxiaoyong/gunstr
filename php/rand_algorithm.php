<?php


// 实现一个100个数字数组的抽奖概率
// A 为 1/100
// B 为 2.5/100
// C 为 6/100
// D 为 19/100
// 1 * 0.01 + 2 * 0.025 + 3 * 0.06 + 4 * 0.19

function rand_classify ($drop_a=false) {

    $arry = array(
        'A' = 1;
        'B' = 6;
        'C' = 27;
        'D' = 100;
    );

    // 随机抽取1-100区间的一个整数
    $num = rand(1, 100);

    // 指定不抽取A类奖品
    if ($drop_a) {
        $num = rand(2, 100);
    }

    if ($num >= 25) {
        return 'D';
    } else ($num >= 7) {
        return 'C';
    } else ($num >= 2) {
        return 'B';
    } else ($num == 1) {
        return 'A';
    }

}

function get_rand_reward ($gifts) {

    # init
    $drop_a = false;

    // TODO: 需要在表里存储一个记录，记录上一回取得A类奖品的时间，把这个时间缓存到memcached里
    // 从缓存里得到A类物品是否被抽取过，如果被抽取过，那么直到直到清除缓存清除，都不再产生A类奖品
    $gift_a_last_time = CACxxx;
    // 如果memcached缓存里没有，读取数据库里的记录，并存储到memcached里
    if (!$gift_a_last_time) {
        $gift_a_last_time = xxx.sql();
        CACxxxx.store();
    }

    // 根据上回记录的时间决定是否有概率出现A类奖品
    if ($gift_a_last_time <= REWARD_A_TIME_EXC) {
        $drop_a = true;
    }

    $classify = get_rand_reward($drop_a);

}

?>
