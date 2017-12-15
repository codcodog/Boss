<?php
/**
 * 数据分析类
 *
 * @author Cryven
 * @date   Thu Dec 14 11:35:40 CST 2017
 */

class Analysis
{
    protected $db          = null;
    protected $sqlite_file = 'boss.db';
    protected $html_file   = 'analysis.html';

    // --------------------------------------------------

    // 初始化
    public function __construct()
    {
        $this->db_conn();
    }

    // --------------------------------------------------

    /**
     * 连接sqlite数据库
     * 
     * @return void
     */
    protected function db_conn()
    {
        try {
            $this->db = new PDO('sqlite:'.$this->sqlite_file);
        } catch (Exception $e) {
            echo '连接错误：' . $e->getMessage();
        }
    }

    // --------------------------------------------------

    /**
     * 查询行业类别
     *
     * @return array
     */
    protected function industry_category()
    {
        $sql  = "select `type`, count(*) as `total` from `boss` group by `type` order by `total`";
        $st   = $this->db->query($sql);

        return $st->fetchAll();
    }

    // --------------------------------------------------

    /**
     * 各区数据
     *
     * @return array
     */
    protected function area()
    {
        $sql = 'select `area`, count(*) as total from `boss` group by `area` order by total DESC';
        $st  = $this->db->query($sql);

        return $st->fetchAll();
    }

    // --------------------------------------------------

    /**
     * 各商圈数据
     *
     * @return array
     */
    protected function business()
    {
        $sql = 'select `business`, count(*) as total from `boss` group by `business` order by total DESC limit 30';
        $st  = $this->db->query($sql, PDO::FETCH_ASSOC);

        return $st->fetchAll();
    }

    // --------------------------------------------------

    /**
     * 各商业区工作年限职位分布
     *
     * @return array
     */
    protected function businessAge($business)
    {
        $sql = 'select age,count(*) as total from boss where business = ? group by age';
        $sth = $this->db->prepare($sql);
        $sth->execute([$business]);

        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }

    // --------------------------------------------------

    /**
     * 获取工作年限分类
     *
     * @return array
     */
    protected function ageType()
    {
        $sql = 'select distinct age from boss';
        $st  = $this->db->query($sql, PDO::FETCH_ASSOC);

        return $st->fetchAll();
    }

    // --------------------------------------------------

    /**
     * 获取商业区薪资
     *
     * @param   string
     * @param   string
     * @return  array
     */
    protected function businessSalary($business, $age)
    {
        $sql = 'select `salary` from `boss` where `business` = ? and `age` = ?';
        $st  = $this->db->prepare($sql);
        $st->execute([$business, $age]);

        return $st->fetchAll(PDO::FETCH_ASSOC);
    }

    // --------------------------------------------------

    /**
     * 获取行业工作年限职位情况
     *
     * @param   string
     * @param   string
     * @return  array
     */
    protected function industryAge($industry) 
    {
        $sql = 'select `age`, count(*) as total from `boss` where `type` = ? group by `age`';
        $st  = $this->db->prepare($sql);
        $st->execute([$industry]);

        return $st->fetchAll(PDO::FETCH_ASSOC);
    }

    // --------------------------------------------------

    /**
     * 获取行业薪资
     *
     * @param   string
     * @param   string
     * @return  array
     */
    protected function industrySalary($industry, $age)
    {
        $sql = 'select `salary` from boss where `type` = ? and `age` = ?';
        $st  = $this->db->prepare($sql);
        $st->execute([$industry, $age]);

        return $st->fetchAll(PDO::FETCH_ASSOC);
    }

    // --------------------------------------------------

    // 各商业区(前15)工作年限分布情况
    protected function business_age()
    {
        $res          = $this->business();
        $res          = array_slice($res, 0, 15);
        $business     = array_column($res, 'business');

        $age_type     = $this->ageType();
        $age_type     = array_column($age_type, 'age');

        $i    = 0;
        $data = [];
        foreach ($age_type as $age) {
            $data[$age] = array_fill(0, 15, 0);
        }
        foreach ($business as $v) {
            $business_res     = $this->businessAge($v);

            foreach ($business_res as $k) {
                foreach ($age_type as $age) {
                    if ($age == $k['age']) {
                        $data[$age][$i] = $k['total']; 
                    }
                }
            }
            $i++;
        }

        return [$age_type, $business, $data];
    }

    // --------------------------------------------------

    // 商业区(前15)工作年限薪资情况
    protected function business_age_salary()
    {
        $res          = $this->business();
        $res          = array_slice($res, 0, 15);
        $business     = array_column($res, 'business');

        $age_type     = $this->ageType();
        $age_type     = array_column($age_type, 'age');

        $i = 0;
        $data = [];
        foreach ($age_type as $age) {
            $data[$age] = array_fill(0, 15, 0);
        }

        foreach ($business as $v) {
            foreach ($age_type as $age) {
                $res1 = $this->businessSalary($v, $age);
                if (empty($res1)) continue;

                $tmp  = [];
                foreach ($res1 as $s) {
                    $tmp[] = intval($s['salary']);
                }

                // 排序，取平均数
                sort($tmp);
                $total = count($tmp);
                if ($total >= 3) {
                    $num = round($total * 0.25);
                    while ($num > 0) {
                        array_pop($tmp);
                        array_shift($tmp);
                        $num--;
                    }
                    $ave = round(array_sum($tmp) / count($tmp));
                } else {
                    $ave = 0;
                }
                $data[$age][$i] = $ave;
            }
            $i++;
        }

        return [$age_type, $business, $data];
    }

    // --------------------------------------------------

    /**
     * 行业工作年限职位发布情况
     *
     * @return  array
     */
    protected function industryWorks()
    {
        $res      = $this->industry_category();
        $industry = array_column($res, 'type');

        $age_type     = $this->ageType();
        $age_type     = array_column($age_type, 'age');

        $i    = 0;
        $data = [];
        foreach ($age_type as $age) {
            $data[$age] = array_fill(0, count($industry), 0);
        }

        foreach ($industry as $v) {
            $res = $this->industryAge($v);

            foreach ($res as $r) {
                foreach ($age_type as $age) {
                    if ($r['age'] == $age) {
                        $data[$age][$i] = $r['total'];
                    }
                }
            }
            $i++;
        }

        return [$industry, $age_type, $data];
    }

    // --------------------------------------------------

    /**
     * 行业薪资情况
     *
     * @return  array
     */
    public function industry_salary()
    {
        $res      = $this->industry_category();
        $industry = array_column($res, 'type');

        $age_type     = $this->ageType();
        $age_type     = array_column($age_type, 'age');

        $i    = 0;
        $data = [];
        foreach ($age_type as $age) {
            $data[$age] = array_fill(0, count($industry), 0);
        }

        foreach ($industry as $v) {
            foreach ($age_type as $age) {
                $res = $this->industrySalary($v, $age);
                if (empty($res)) continue;

                $tmp = [];
                foreach ($res as $r) {
                    $tmp[] = intval($r['salary']);
                }
                
                // 排序， 取平均数
                sort($tmp);
                $total = count($tmp);
                if ($total > 3) {
                    $num = round($total * 0.25);

                    while ($num > 0) {
                        array_pop($tmp);
                        array_shift($tmp);
                        $num--;
                    }
                    $ave = round(array_sum($tmp) / count($tmp));
                } else {
                    $ave = 0;
                }
                $data[$age][$i] = $ave;
            }
            $i++;
        }

        return [$age_type, $industry, $data];
    }

    // --------------------------------------------------

    // 数据展示
    public function show()
    {
        $area_data     = json_encode($this->area());
        $business_data = json_encode($this->business());
        $industry_data = json_encode($this->industry_category());

        list($age_type, $business, $data) = $this->business_age();
        $age_type                         = json_encode(array_keys($age_type));
        $business_type                    = json_encode($business);
        $data                             = json_encode($data);

        list($age_type5, $business5, $data5) = $this->business_age_salary();
        $age_type5                         = json_encode(array_keys($age_type5));
        $business_type5                    = json_encode($business5);
        $data5                             = json_encode($data5);

        list($industry6, $age6, $data6) = $this->industryWorks();
        $industry6                      = json_encode($industry6);
        $age6                           = json_encode($age6);
        $data6                          = json_encode($data6);

        list($age7, $industry7, $data7) = $this->industry_salary();
        $age7                           = json_encode($age7);
        $industry7                      = json_encode($industry7);
        $data7                          = json_encode($data7);

        // php变量赋值给js
        $js_code = <<< JAVASCRIPT
<script type='text/javascript'>

var area         = $area_data;
var business     = $business_data;
var industry     = $industry_data;

var age_type     = $age_type;
var type4        = $business_type;
var data4        = $data;

var age_type5    = $age_type5;
var type5        = $business_type5;
var data5        = $data5;

var industry6    = $industry6;
var age6         = $age6;
var data6        = $data6;

var industry7    = $industry7;
var age7         = $age7;
var data7        = $data7;

</script>
JAVASCRIPT;

        echo $js_code;
        include $this->html_file;
    }
}

$a = new Analysis;
$a->show();
