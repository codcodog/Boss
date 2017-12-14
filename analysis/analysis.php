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
    public function area()
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
    public function business()
    {
        $sql = 'select `business`, count(*) as total from `boss` group by `business` order by total DESC limit 30';
        $st  = $this->db->query($sql);

        return $st->fetchAll();
    }

    // --------------------------------------------------

    // 数据展示
    public function show()
    {
        $area_data     = json_encode($this->area());
        $business_data = json_encode($this->business());
        $industry_data = json_encode($this->industry_category());

        // php变量赋值给js
        $js_code = <<< JAVASCRIPT
<script type='text/javascript'>

var area     = $area_data;
var business = $business_data;
var industry = $industry_data;

</script>
JAVASCRIPT;

        echo $js_code;
        include $this->html_file;
    }
}



$a = new Analysis;
$a->show();
